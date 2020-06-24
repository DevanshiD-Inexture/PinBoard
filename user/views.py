from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Account
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (UserRegisterForm,
					UserUpdateForm,
					UserAccountUpdateForm,
					ProfileUpdateForm,
					AccountUpdateForm)
from collection.models import Collection, Pin

class ProfileFollowView(View, LoginRequiredMixin):
	def post(self, request, *args, **kwargs):
		# print(request.POST)
		username_to_toggle = request.POST.get('username')
		profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
		return redirect(f'/profile-detail/{profile_.user.username}/')


def home(request):

	context = {
		'pins' : Pin.objects.all()
	}
	return render(request, 'user/home.html', context)


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()

			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'user/register.html', {'form' : form})

@login_required
def profile(request):

	return render(request, 'user/profile.html')

@login_required
def edit_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance = request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been Updated!')
			return redirect('edit_profile')

	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)

	context = {
		'u_form' : u_form,
		'p_form' : p_form
	}
	return render(request, 'user/edit_profile.html', context)

@login_required
def account(request):
	if request.method == 'POST':
		u_form = UserAccountUpdateForm(request.POST, instance = request.user)
		a_form = AccountUpdateForm(request.POST, instance = request.user.account)
		if u_form.is_valid() and a_form.is_valid():
			u_form.save()
			a_form.save()
			messages.success(request, f'Your account has been Updated!')
			return redirect('account')

	else:
		u_form = UserAccountUpdateForm(instance = request.user)
		a_form = AccountUpdateForm(instance = request.user.account)

	context = {
		'u_form' : u_form,
		'a_form' : a_form
	}
	return render(request, 'user/account.html', context)

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('change_password')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'user/change_password.html', {'form': form})

@login_required
def settings(request):

	return render(request, 'user/settings.html')

class ProfileDetailView(DetailView):
	model = Profile
	template_name = 'user/user_profile.html'

	def get_object(self):
		username = self.kwargs.get("username")
		if username is None:
			raise Http404
		return get_object_or_404(User, username__iexact=username, is_active=True)

	def get_context_data(self, *args, **kwargs):
		context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
		user = context['user']
		is_following = False
		if user.profile in self.request.user.is_following.all():
			is_following = True
		context['is_following'] = is_following
		qs = Profile.objects.filter(user=user)
		if qs.exists():
			context['profile'] = qs
		return context