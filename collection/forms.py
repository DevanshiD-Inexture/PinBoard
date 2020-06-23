from django import forms
from django.contrib.auth.models import User
from .models import Collection, Pin

class PinCreateForm(forms.ModelForm):

    class Meta:
        model = Pin
        fields = ['title', 'detail', 'image', 'collection']