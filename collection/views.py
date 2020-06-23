from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
	 ListView, 
	 DetailView, 
	 CreateView,
	 UpdateView, 
	 DeleteView
)
from .models import Collection

class CollectionListView(ListView):
	model = Collection
	template_name = 'user/home.html'
	context_object_name = 'collections'
	ordering = ['-date_created']


class CollectionDetailView(DetailView):
	model = Collection

class UserCollectionView(ListView):
	model = Collection
	template_name = 'collection/user_collection.html'
	context_object_name = 'collections'

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Collection.objects.filter(owner = user).order_by('-date_created')

class CollectionCreateView(LoginRequiredMixin, CreateView):
	model = Collection
	fields = ['name', 'description']

	def form_valid(self, form):
		print(form)
		print(form.is_valid())
		form.instance.owner = self.request.user
		return super().form_valid(form)

class CollectionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Collection
	fields = ['name', 'description']

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

	def test_func(self):
		collection = self.get_object()
		if self.request.user == collection.owner:
			return True
		return False

class CollectionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Collection
	success_url = '/'
	
	def test_func(self):
		collection = self.get_object()
		if self.request.user == collection.owner:
			return True
		return False

# class PinListView(ListView):
# 	model = Pin
# 	template_name = 'user/home.html'
# 	context_object_name = 'pins'
# 	ordering = ['-date_created']


# class PinCreateView(LoginRequiredMixin, CreateView):
# 	model = Pin
# 	fields = ['title', 'description', 'image']

# 	def form_valid(self, form):
# 		form.instance.owner = self.request.user
		
# 		return super().form_valid(form)		

# @login_required
# def create_pin(request):
# 	if request.method == 'POST':
# 		form = PinCreateForm(request.POST)
# 		print(form)
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request, f'Your Pin has been Created!')
# 			return redirect('home')
# 		else:
# 			print("Not Valid")
# 	else:
# 		form = PinCreateForm()
	
# 	return render(request, 'collection/pin_form.html', {'form' : form})