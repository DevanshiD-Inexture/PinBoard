from django.conf import settings
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
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
	image = models.ImageField(upload_to='my_pins')
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('pin-detail', kwargs={"pk": self.pk})

class Comment(models.Model):
	pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField(max_length=255)
	date_comented = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return '{}-{}'.format(self.pin.title, str(self.user.username))

	def get_absolute_url(self):
		return reverse('comment-detail', kwargs = {'pk':self.pk})

