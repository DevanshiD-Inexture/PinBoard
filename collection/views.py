from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
	 ListView, 
	 DetailView, 
	 CreateView,
	 UpdateView, 
	 DeleteView
)

from .models import Collection

# Create your views here.

class CollectionDetailView(DetailView):
	model = Collection


class CollectionCreateView(LoginRequiredMixin, CreateView):
	model = Collection
	fields = ['name', 'description']

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)
