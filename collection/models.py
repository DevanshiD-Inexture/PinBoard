from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Collection(models.Model):
	
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)	
	description = models.TextField(blank=True, max_length=255)
	date_created = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('collection-detail', kwargs = {'pk':self.pk})

class Pin(models.Model):

	title = models.CharField(max_length=100, blank=True)
	detail = models.TextField(blank=True, max_length=255)
	date_posted = models.DateTimeField(default=timezone.now)
	image = models.ImageField(upload_to='my_pins')
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title