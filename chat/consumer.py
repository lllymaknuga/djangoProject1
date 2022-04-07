import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from chat.models import City
from chat.serializer import MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        room = City.objects.get(name=self.scope['url_route']['kwargs']['room_name']).id
        self.user_id = self.scope['user']
        self.room_name = room
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def websocket_disconnect(self, message):
        print(message)
        super(ChatConsumer, self).websocket_disconnect(message)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_pk = self.room_name
        user = Token.objects.get(key=text_data_json['token']).user
        print(user)
        message_serializer = MessageSerializer(data={'content': message, 'city_id': room_pk, 'user': user.id})
        if message_serializer.is_valid():
            message_serializer.save()
            print(message_serializer.data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'date': message_serializer.data['created_at'],
                    'user-id': user.id,
                    'username': user.username,
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        date = event['date']
        self.send(text_data=json.dumps({
            'message': message,
            'date': date,
            'user_id': event['user-id'],
            'username': event['username']
        }))  # Receive message from room group
