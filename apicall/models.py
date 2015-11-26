from django.db import models
from django.utils import timezone

# Create your models here.
class Log(models.Model):
	userip = models.CharField(max_length=64)
	visited = models.DateTimeField(default=timezone.now)
		
class Link(models.Model):
	created = models.DateTimeField(default=timezone.now)
	linkip = models.CharField(max_length=64)
	linktext = models.CharField(max_length=500)
	linktype = models.CharField(max_length=1) #i=image; a=audio; v=video
