from django.urls import path, re_path

from .views import ThreadView, InboxView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view(template_name='chat/inbox.html'), name='user-inbox'),
    re_path(r"^(?P<username>[\w.@+-]+)/", ThreadView.as_view(template_name='chat/thread_list.html'), name='chat-detail'),
]