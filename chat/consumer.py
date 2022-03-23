import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import City
from chat.serializer import MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        room = City.objects.get(name=self.scope['url_route']['kwargs']['room_name']).id
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
        print(text_data_json)
        message = text_data_json['message']
        token = text_data_json['token']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'room': self.room_name,
                'token': token
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print(event)
        message = event['message']
        room_pk = event['room']
        print(room_pk)
        message_serializer = MessageSerializer(data={'content': message, 'city_id': room_pk})
        print(message_serializer.is_valid())
        if message_serializer.is_valid():
            message_serializer.save()
        self.send(text_data=json.dumps({
            'message': message,
            'date': message_serializer.data['created_at'],
            'token': event['token']
        }))  # Receive message from room group
