# -*- coding: utf-8 -*-
import json, requests, os
import html, random
from requests_futures.sessions import FuturesSession
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from .models import Log, Link
from .forms import ImageLinkForm, AudioLinkForm, VideoLinkForm, SentiForm, LangForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOSHARE_PATH = os.path.join(BASE_DIR, "noshare")


def gimmeip(request):
	"""
		This is NOT A VIEW.
		Returns the IP of the requester (user), accounting for the possibility of being behind a proxy.
	"""
	ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
	if ip:
	# X_FORWARDED_FOR returns client1, proxy1, proxy2,...
		ip = ip.split(", ")[0]
	else:
		ip = request.META.get("REMOTE_ADDR", "")
	return ip

def gimmeapikey(request):
    """
		This is NOT A VIEW.
        Returns apikey
    """
    with open(os.path.join(NOSHARE_PATH, "api_key.txt"), 'r') as f:
        API_KEY = f.read()
    return API_KEY

def check_result(request):
	"""
		This is NOT A VIEW.
		Returns the job status after querying asynchronously. If finished, returns result.
	"""
	API_KEY = gimmeapikey(request)
	jobid = request.session['jobid']
	payload = {'apikey':API_KEY}
	session = FuturesSession()
	
	try:
		future = session.post('https://api.havenondemand.com/1/job/status/'+jobid, data = payload)
		r = future.result()
	except Exception as e:    # This is the correct syntax
		return 0
		
	# check if response if valid, else return error.
	
	# r.content is a byte array. To cure that, decode utf-8 is used.
	
	response = r.content.decode('utf-8')
	json_data = json.loads(response)
	
	if 'status' in json_data:
		if json_data['status'] == 'finished':
			request.session['extracted_text'] = json_data['actions'][0]['result']['document'][0]['content']
		return json_data['status']
	else:
		return 0
	
	
def ip_view(request):
	"""
		Returns the IP of the request, accounting for the possibility of being behind a proxy.
    """
	ip = gimmeip(request)
	Log.objects.create(userip=ip)
	return render(request, 'apicall/index.html')

def link_submit_view(request):
	"""
		Stores image, audio or video link to db, redirects to respective page.
	"""
	request.session.set_expiry(2000)
	ip = gimmeip(request)
		
	if request.method == 'POST':
		# check if linktype is i, a or v
		ltype = request.POST['linktype']
		if ltype == 'i':
			form = ImageLinkForm(request.POST)
		elif ltype == 'a':
			form = AudioLinkForm(request.POST)
		elif ltype == 'v':
			form = VideoLinkForm(request.POST)
		if form.is_valid():				
			newlink = Link(linkip = ip, linktext = request.POST['linktext'].strip(), linktype = request.POST['linktype'] )
			# save this new link in the model/db.
			newlink.save()
            # Redirect to the extracted text page after saving link
			if ltype == 'i':
				return HttpResponseRedirect(reverse('image_out_view'))
			else:
				return HttpResponseRedirect(reverse('av_processing_view'))
		
	else:
		form = ImageLinkForm()

	return render(request, 'apicall/image_input.html', {'form':form})
	
def image_input_view(request):
	"""
		Returns a form to take input of the image url
	"""
	form = ImageLinkForm()
	return render(request, 'apicall/image_input.html', {'form':form})

def audio_input_view(request):
	"""
		Returns a form to take input of the audio url
	"""
	form = AudioLinkForm()
	return render(request, 'apicall/audio_input.html', {'form':form})	

def video_input_view(request):
	"""
		Returns a form to take input of the video url
	"""
	form = VideoLinkForm()
	return render(request, 'apicall/video_input.html', {'form':form})
	
	
def image_out_view(request):
	"""
		Returns extracted text from image.
	"""
	ip = gimmeip(request)
	
	# Take the latest 'image' link submitted by this ip/user.
	latest_link = Link.objects.filter(linkip=ip, linktype='i').order_by('-created')[0].linktext

	if latest_link:
		API_KEY = gimmeapikey(request)
		
		imglink =  latest_link.strip()	 
		payload = {'apikey':API_KEY, 'url':imglink}
		
		try:
			r = requests.post("https://api.havenondemand.com/1/api/sync/ocrdocument/v1", data = payload)
		except requests.exceptions.RequestException as e:    # This is the correct syntax
			return HttpResponseRedirect(reverse('error'))
		
		#print(imglink)
		if r.status_code == requests.codes.ok:
			data = r.text
			# cleaning response, manually ofcourse, I'm <i>that</i> good.
			data = data[:30]+data[30:].replace('\n', '\r\n')
			json_data = json.loads(data)
			text = json_data['text_block'][0]['text']
			text = html.unescape(text)
			
			# setting session variable which carries extracted text from image. Used later for sentiment analysis etc
			request.session['extracted_text'] = text
			
			return render(request, 'apicall/image_out.html', {'text': text, 'link' : imglink})
			
		else:
			return HttpResponseRedirect(reverse('error'))
	else:
		return HttpResponseRedirect(reverse('error'))
		
def av_processing_view(request):
	"""
		Inputs a audio link, stores jobid to dict, redirects to processing page.
	"""
	ip = gimmeip(request)
	
	# no need to store linkid when jobid is required in every step. store only jobid instead.
	#latest_link_id = Link.objects.filter(linkip=ip, linktype='a').order_by('-created')[0].id
	latestlink = Link.objects.filter(linkip=ip).exclude(linktype='i').order_by('-created')[0].linktext
	
	#check if latest_link exists
	if latestlink:
		
		API_KEY = gimmeapikey(request)
		
		latest_link = latestlink.strip()	 
		payload = {'apikey':API_KEY, 'url':latest_link}

		
		session = FuturesSession()
		try:
			future = session.post('https://api.havenondemand.com/1/api/async/recognizespeech/v1', data = payload)
			r = future.result()
		except Exception as e:    # This is the correct syntax
			return 0
		
		# r.content is a byte array. To cure that, decode utf-8 is used.
		
		response = r.content.decode('utf-8')
		#this works too, to get jobID string
		#response = str(r.result().content)[2:-1]
		
		json_data = json.loads(response)
		
		
		if 'jobID' in json_data:
			jobid = json_data['jobID']
			# setting jobid and linktext as session variables. 
			request.session['jobid'] = jobid
			request.session['linktext'] = latest_link
			
		return render(request, 'apicall/av_processing.html', { 'link' : latest_link, 'status': 'Processing...'})
		
	else:
		return HttpResponseRedirect(reverse('error'))

def av_out_view(request):
	"""
		Returns the extracted text from image and video urls.
	"""
	return render(request, 'apicall/av_out.html', { 'link' : request.session['linktext'], 'text': request.session['extracted_text']})
	

def check_result_view(request):
	"""
		Checks if the audio or video file has been transcibed. Displays result.
	"""
	status = check_result(request)
	custom_status = ''
	statuslist = ['Obliging your request', 'Just a second', 'Squeezing out Text', 'The wait is worth it', 'Waiting for postman', 'It is coming', 'Patience is key', 'Wait for it', 'Text is omnipresent', 'No wait no Gain', 'Hi there, Coffee?', 'Don\'t sleep yet', 'I can almost see it', 'Wait is almost over', 'Just around the corner', 'Forging Valyrian Steel', 'In Queue', 'Readying horses', 'Just one more click', 'Just two more clicks', 'oo, nice text', 'Hello there!', 'Gathering Text', 'Should\'ve bought pro version', 'Changing Oil, Filling Tyres', 'Confucius say, "Text"']
	if status:
		if status == 'finished':
			return HttpResponseRedirect(reverse('av_out_view'))
		else:
			if status == 'queued':
				custom_status = random.choice(statuslist)
			return render(request, 'apicall/av_processing.html', { 'link' : request.session['linktext'], 'status': status, 'custom_status':custom_status})
	else:
		return HttpResponseRedirect(reverse('error'))
		
def sentiment_input_view(request):
	"""
		Takes extracted text(if available) from a session variable, autofills it in text field.
	"""
	form = SentiForm(request)
	if 'extracted_text' in request.session:
		extracted_text = request.session['extracted_text']
		return render(request, 'apicall/sentiment_input.html', {'form':form, 'extracted_text':extracted_text})
	else:
		return render(request, 'apicall/sentiment_input.html', {'form':form, 'extracted_text':''})
		
def sentiment_out_view(request):
	"""
		Returns the sentiment and score of the input text
	"""
	API_KEY = gimmeapikey(request)
		

	if request.method == 'POST':
		form = SentiForm(request, request.POST)
		if form.is_valid():
			inptext = form.cleaned_data['inptext']
			lang = form.cleaned_data['lang']
			payload = {'apikey':API_KEY, 'text':inptext, 'language':lang}
			try:
				r = requests.post("https://api.havenondemand.com/1/api/sync/analyzesentiment/v1", data = payload)
			except requests.exceptions.RequestException as e:    # This is the correct syntax
				return HttpResponseRedirect(reverse('error'))
			
			l = {'eng': 'English','fre': 'French','spa': 'Spanish', 'ger': 'German','ita': 'Italian','chi': 'Chinese', 'por': 'Portugese','dut': 'Dutch','rus': 'Russian','cze': 'Czech','tur': 'Turkish'}
			language = l[lang]
			
			if r.status_code == requests.codes.ok:
				data = r.text
				
				json_data = json.loads(data)
				jd = dict(json_data)
				score = str(jd['aggregate']['score'])[:5]
				senti = jd['aggregate']['sentiment']
			
				return render(request, 'apicall/sentiment_out.html', {'text': inptext, 'lang':language, 'agg': score, 'senti': senti})
			else:
				return HttpResponseRedirect(reverse('error'))
	else:
		form = SentiForm(request)
	return render(request, 'apicall/sentiment_input.html', {'form':form})

def language_input_view(request):
	"""
		Inputs text for Language detection.
	"""
	form = LangForm(request)
	if 'extracted_text' in request.session:
		extracted_text = request.session['extracted_text']
		return render(request, 'apicall/language_input.html', {'form':form, 'extracted_text':extracted_text})
	else:
		return render(request, 'apicall/language_input.html', {'form':form, 'extracted_text':''})
		
def language_out_view(request):
	"""
		Returns the language and encoding of the input text.
	"""
	API_KEY = gimmeapikey(request)
		
	if request.method == 'POST':
		form = LangForm(request, request.POST)
		if form.is_valid():
			inptext = form.cleaned_data['inptext']
			payload = {'apikey':API_KEY, 'text':inptext}
			try:
				r = requests.post("https://api.havenondemand.com/1/api/sync/identifylanguage/v1", data = payload)
			except requests.exceptions.RequestException as e:    # This is the correct syntax
				return HttpResponseRedirect(reverse('error'))
			
			if r.status_code == requests.codes.ok:
				data = r.text
				
				json_data = json.loads(data)
				jd = dict(json_data)
				lang = jd['language']
				enc = jd['encoding']
				return render(request, 'apicall/language_out.html', {'text': inptext, 'lang':lang, 'enc':enc})
			else:
				return HttpResponseRedirect(reverse('error'))
	else:
		form = LangForm(request)
	return render(request, 'apicall/language_input.html', {'form':form})

		
def error_view(request):
	"""
		Returns a static Error Page.
	"""
	return render(request, 'apicall/error.html')
	
def terms_view(request):
	"""
		Returns a static Terms Of Service Page.
	"""
	return render(request, 'apicall/terms.html')