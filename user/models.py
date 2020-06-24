from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from PIL import Image

class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	followers = models.ManyToManyField(User, related_name='is_following', blank=True)
	activated = models.BooleanField(default=False)
	about = models.TextField(blank=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pic')
	location = models.CharField(max_length=30, blank=True, null=True)
	
	objects = ProfileManager()

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
	country = CountryField(blank=True, null=True)
	GENDER = (
		('m', 'Male'),
		('f', 'Female'),
		('o', 'Other'),
	)
	gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)

	def __str__(self):
		return f'{self.user.username} Account'