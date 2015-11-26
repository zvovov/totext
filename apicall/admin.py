from django.contrib import admin

# Register your models here.
from apicall.models import Log, Link


class LogAdmin(admin.ModelAdmin):
	fieldsets = [
	('User IP', 			{'fields': ['userip']}),
	('Date Information', 	{'fields': ['visited']}),
	]
	list_display = ('id', 'userip', 'visited')
	
class LinkAdmin(admin.ModelAdmin):
	fieldsets = [
	('User IP', 			{'fields': ['linkip']}), 
	('Link',				{'fields': ['linktext']}), 
	('Type',				{'fields': ['linktype']}),
	('Date Information',	{'fields': ['created']}),
	]
	list_display = ('id', 'linkip', 'linktext', 'linktype', 'created')
	
admin.site.register(Log, LogAdmin)
admin.site.register(Link, LinkAdmin)