from django import forms
from django.contrib.auth.models import User
from .models import Collection, Pin

class PinCreateForm(forms.ModelForm):


	class Meta:
		model = Pin
		fields = ['title', 'detail', 'image', 'collection']

	def __init__(self, user, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PinCreateForm, self).__init__(*args, **kwargs)
		self.fields['collection'].queryset = Collection.objects.filter(owner = user)