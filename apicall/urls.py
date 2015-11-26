# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url

urlpatterns = patterns('apicall.views',
	url(r'^linksubmit/$', 'link_submit_view', name='link_submit_view'),

	url(r'^image/$', 'image_input_view', name='image_input_view'),
	url(r'^image$', 'image_input_view', name='image_input_view'),
	url(r'^image/extract/$', 'image_out_view', name='image_out_view'),

	url(r'^audio/$', 'audio_input_view', name='audio_input_view'),
	url(r'^audio$', 'audio_input_view', name='audio_input_view'),
	url(r'^video/$', 'video_input_view', name='video_input_view'),
	url(r'^video$', 'video_input_view', name='video_input_view'),


	url(r'^file/processing/$', 'av_processing_view', name='av_processing_view'),
	url(r'^file/processing/check/$', 'check_result_view', name='check_result_view'),
	url(r'^file/processed/$', 'av_out_view', name='av_out_view'),

	url(r'^sentiment/$', 'sentiment_input_view', name='sentiment_input_view'),
	url(r'^sentiment$', 'sentiment_input_view', name='sentiment_input_view'),
	url(r'^sentiment/result/$', 'sentiment_out_view', name='sentiment_out_view'),

	url(r'^language/$', 'language_input_view', name='language_input_view'),
	url(r'^language$', 'language_input_view', name='language_input_view'),
	url(r'^language/result/$', 'language_out_view', name='language_out_view'),

	url(r'^error$', 'error_view', name='error'),
	url(r'^terms$', 'terms_view', name='terms'),

	url(r'^$', 'ip_view', name='index'),
	url(r'', 'error_view', name='error')
)


