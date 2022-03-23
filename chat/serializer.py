from rest_framework.serializers import ModelSerializer

from chat.models import City, Message


class CitySerializer(ModelSerializer):
    class Meta:
        fields = ['name']
        model = City


class MessageSerializer(ModelSerializer):
    class Meta:
        fields = ['content', 'city_id', 'id', 'created_at']
        read_only_fields = ['id', 'created_at']
        model = Message

    def save(self, **kwargs):
        print(self.validated_data)
        super().save(**kwargs)
