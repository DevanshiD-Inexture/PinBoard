from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Collection(models.Model):
	
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)	
	description = models.TextField(blank=True)
	date_created = models.DateTimeField(default = timezone.now)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('collection-detail', kwargs = {'pk':self.pk})
