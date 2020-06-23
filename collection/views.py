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
	 DeleteView,
	 RedirectView
)
from collection.models import Collection, Pin
from collection.forms import PinCreateForm, PinUpdateForm

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

class PinListView(ListView):
	model = Pin
	template_name = 'user/home.html'
	context_object_name = 'pins'
	ordering = ['-date_created']

class PinDetailView(DetailView):
	model = Pin

class UserPinView(ListView):
	model = Pin
	template_name = 'collection/user_pin.html'
	context_object_name = 'pins'

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Pin.objects.filter(author = user).order_by('-date_posted')

@login_required
def create_pin(request):
	if request.method == 'POST':

		form = PinCreateForm(request.user, request.POST, request.FILES)

		if form.is_valid():
			pin = form.save(commit=False)
			pin.author = request.user
			pin.save()
			
			messages.success(request, f'Your Pin has been Created!')
			return redirect('home')
		
	else:
		form = PinCreateForm(request.user)
	
	return render(request, 'collection/pin_form.html', {'form' : form})

@login_required
def edit_pin(request, pk):
	pin = get_object_or_404(Pin, pk=pk)    
	form = PinUpdateForm(request.user, request.POST or None, instance=pin)

	if form.is_valid():
		form.save()
		messages.success(request, f'Your pin details has been Updated!')
		return redirect('home')
	
	context = {
		'form' : form
	}
	return render(request, 'collection/pin_update.html', context)

@login_required
def delete_pin(request, pk):
	pin = get_object_or_404(Pin, pk=pk)    
	if request.method=='POST':
		pin.delete()
		return redirect('home')
	return render(request, 'collection/pin_confirm_delete.html', {'object':pin})

class PinLikeToggle(RedirectView, LoginRequiredMixin):
	def get_redirect_url(self, *args, **kwargs):
		pk = self.kwargs.get("pk")
		obj = get_object_or_404(Pin, pk=pk)
		url_ = obj.get_absolute_url()
		user = self.request.user
		if user in obj.likes.all():
			obj.likes.remove(user)
		else:
			obj.likes.add(user)
		return url_
