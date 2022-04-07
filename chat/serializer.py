from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from chat.models import City, Message
from users.models import CustomUser


class CitySerializer(ModelSerializer):
    class Meta:
        fields = ['name']
        model = City


class MessageSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        fields = ['content', 'city_id', 'created_at', 'user', 'username', 'id']
        read_only_fields = ['id', 'created_at', 'username']
        model = Message

    def save(self, **kwargs):
        print(self.validated_data)
        super().save(**kwargs)
