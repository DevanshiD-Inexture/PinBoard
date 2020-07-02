from django.urls import path, re_path

from .views import ThreadView, InboxView, NotificationListView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view(template_name='chat/inbox.html'), name='user-inbox'),
    path("notification/", NotificationListView.as_view(template_name='chat/notification.html'), name='user-notification'),
    re_path(r"^(?P<username>[\w.@+-]+)/", ThreadView.as_view(template_name='chat/thread_list.html'), name='chat-detail'),
]