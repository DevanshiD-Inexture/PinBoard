from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from chat.forms import ComposeForm
from chat.models import Thread, ChatMessage

class InboxView(LoginRequiredMixin, ListView):
	model = Thread
	template_name = 'chat/inbox.html'
	context_object_name = 'rooms_list'
	ordering = ['-timestamp']

	def get(self, request, *args, **kwargs):
		rooms_list = Thread.objects.by_user(self.request.user)
		if rooms_list.exists():
			context = {
				'rooms_list' : rooms_list
			}
			return render(request, 'chat/inbox.html', context= context)

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
	template_name = 'chat/thread_list.html'
	form_class = ComposeForm
	success_url = './'

	def get_queryset(self):
		return Thread.objects.by_user(self.request.user)

	def get_object(self):
		other_username = self.kwargs.get("username")

		obj, created = Thread.objects.get_or_new(self.request.user, other_username)
		if obj == None:
			raise Http404
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()
		form = self.get_form()
		
		if form.is_valid():
			message = form.cleaned_data['message']
			message.save()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		thread = self.get_object()
		user = self.request.user
		message = form.cleaned_data.get("message")
		ChatMessage.objects.create(user=user, thread=thread, message=message)
		return super().form_valid(form)