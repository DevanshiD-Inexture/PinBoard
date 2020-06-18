from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from PIL import Image


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	about = models.TextField(blank=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pic')
	location = models.CharField(max_length=30, blank=True)
	
	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kawrgs):
		super().save(*args, **kawrgs)

		img = Image.open(self.image.path)

		if img.height > 600 or img.width > 600:
			output_size = (600, 600)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	country = CountryField()
	GENDER = (
		('m', 'Male'),
		('f', 'Female'),
		('o', 'Other'),
	)
	gender = models.CharField(max_length=1, choices=GENDER)

	def __str__(self):
		return f'{self.user.username} Account'

