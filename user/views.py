from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Account
from .forms import (UserRegisterForm, 
					UserUpdateForm,
					UserAccountUpdateForm, 
					ProfileUpdateForm, 
					AccountUpdateForm)

def home(request):
	
	return render(request, 'user/home.html')


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
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
		p_form = AccountUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been Updated!')
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