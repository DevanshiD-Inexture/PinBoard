from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.conf.urls import url
from chat.consumers import ChatConsumer, NotificationConsumer

application = ProtocolTypeRouter({
    'websocket' : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path("messages/notification/", NotificationConsumer),
                    path("messages/<str:username>/", ChatConsumer),
                    
                    # url(r"^messages/notification/$", ChatConsumer),
                ]
            )
        )
    )
})