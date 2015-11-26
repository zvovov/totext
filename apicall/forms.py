from django import forms
from .models import Link

class ImageLinkForm(forms.Form):	
	linktext = forms.CharField(max_length=500, label = "Link:", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Link', 'type':'url'}))
	linktype = forms.ChoiceField(choices=[('i', '')], widget=forms.RadioSelect(attrs={'checked':'checked', 'class':'hiddenfield'}))

class AudioLinkForm(forms.Form):
	linktext = forms.CharField(max_length=500, label = "Link:", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Link', 'type':'url'}))
	linktype = forms.ChoiceField(choices=[('a', '')], widget=forms.RadioSelect(attrs={'checked':'checked', 'class':'hiddenfield'}))	
	
class VideoLinkForm(forms.Form):
	linktext = forms.CharField(max_length=500, label = "Link:", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Link', 'type':'url'}))
	linktype = forms.ChoiceField(choices=[('v', '')], widget=forms.RadioSelect(attrs={'checked':'checked', 'class':'hiddenfield'}))	
	
class SentiForm(forms.Form):
	def __init__(self,request,*args,**kwargs):
		if 'extracted_text' in request.session:
			ext_text = request.session['extracted_text']
		else:
			ext_text = ''
		super(SentiForm,self).__init__(*args,**kwargs)
		ch=[('eng', 'English'),('fre', 'French'),('spa', 'Spanish'), ('ger', 'German'),('ita', 'Italian'),('chi', 'Chinese'), ('por', 'Portugese'),('dut', 'Dutch'),('rus', 'Russian'),('cze', 'Czech'),('tur', 'Turkish')]
		self.fields['inptext'] = forms.CharField(label="Input Text:", initial=ext_text, widget=forms.Textarea(attrs={'class':'form-control', 'id':'inptext'}))
		self.fields['lang'] = forms.ChoiceField(choices=ch, widget=forms.Select(attrs={'class':'btn btn-info dropdown-toggle', 'type':'button', 'data-toggle':'dropup'}))
		
class LangForm(forms.Form):
	def __init__(self,request,*args,**kwargs):
		if 'extracted_text' in request.session:
			ext_text = request.session['extracted_text']
		else:
			ext_text = ''
		super(LangForm,self).__init__(*args,**kwargs)
		self.fields['inptext'] = forms.CharField(label="Input Text:", initial=ext_text, widget=forms.Textarea(attrs={'class':'form-control', 'id':'inptext'}))