from django import forms
from .models import ChatMessage

class ComposeForm(forms.ModelForm):
	class Meta:
		model = ChatMessage
		fields = ['message']