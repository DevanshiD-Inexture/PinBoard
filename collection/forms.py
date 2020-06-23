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

class PinUpdateForm(forms.ModelForm):

	class Meta:
		model = Pin
		fields = ['title', 'detail', 'collection']		

	def __init__(self, user, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PinUpdateForm, self).__init__(*args, **kwargs)
		self.fields['collection'].queryset = Collection.objects.filter(owner = user)

	def test_func(self, user):
		pin = self.get_object()
		if user == pin.author:
			return True
		return False

