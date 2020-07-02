import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Thread, ChatMessage, Notification

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
          "type" : "websocket.accept"  
        })
        
        # self.message.reply_channel.send({"accept": True})
    async def websocket_receive(self, event):
        print("receive", event)

        # message_type = event.get('type', None)  #check message type, act accordingly
        message_type = json.loads(event.get('text', None)).get('type')
        print(message_type)
        if message_type == "notification_read":
            # Update the notification read status flag in Notification model.
            notification = Notification.objects.get(id=notification_id)
            notification.notification_read = True
            notification.save()  #commit to DB
            print("notification read")
            return

        front_text = event.get('text', None)
        if front_text is not None:
            loaded_data = json.loads(front_text)
            msg = loaded_data.get('message')
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                'message' : msg,
                'username' : username
            }

            await self.create_chat_message(user, msg)

            other_user = self.scope['url_route']['kwargs']['username']
            await self.create_notification(other_user=other_user, msg=msg)

            # broadcasts the message event to be sent

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type" : "chat_message",
                    "text": json.dumps(myResponse)
                }
            )

    async def chat_message(self,event):
        
        # send message
        await self.send({
            "type" : "websocket.send",
            "text" : event['text']
        })
        
    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, user, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=user, message=msg)        

    @database_sync_to_async
    def create_notification(self, other_user, msg):
        last_chat = ChatMessage.objects.latest('id')
        print(last_chat)
        user = User.objects.get(username=other_user)
        print(user)
        created_notification = Notification.objects.create(notification_user=user, notification_chat=last_chat)
        return created_notification

class NotificationConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)

        await self.send({
          "type" : "websocket.accept"  
        })

    async def websocket_receive(self, event):
        print("receive", event)

        # message_type = event.get('type', None)  #check message type, act accordingly
        message_type = json.loads(event.get('text', None)).get('type')
        notification_id = json.loads(event.get('text', None)).get('notification_id')
        print(notification_id)
        print(message_type)
        if message_type == "notification_read":
            # Update the notification read status flag in Notification model.
            await self.change_notification_status(notification_id)
            
    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def change_notification_status(self, notification_id):
        notification = Notification.objects.get(id=notification_id)
        notification.notification_read = True
        notification.save()  #commit to DB
        notification.delete()
        print("notification read")
        return
