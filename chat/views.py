from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from chat.models import Message, City
from chat.serializer import MessageSerializer, CitySerializer


def index(request):
    return render(request, '../../djangoProject1/templates/index.html')


def room(request, room_name):
    return render(request, '../../djangoProject1/templates/room.html', {
        'room_name': room_name
    })


class MessageApiList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        city = self.request.GET['city']
        queryset = self.queryset.filter(city_id__name=city)
        try:
            id_message = int(self.request.GET['message'])
        except KeyError:
            id_message = queryset.count()
        print(id_message)
        if 9 >= id_message:
            return queryset[0:id_message]
        if queryset.count() == 0:
            return []
        lst = queryset[id_message - 10:id_message]
        print(lst)
        return lst

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            id_message = int(self.request.GET['message'])
        except KeyError:
            id_message = len(self.queryset.all())
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({'messages': serializer.data, 'id_message': -1})
        if 9 >= id_message:
            return Response({'messages': serializer.data, 'id_message': -1})
        if id_message == 0:
            return Response({'messages': serializer.data, 'id_message': -1})
        print(id_message)
        return Response({'messages': serializer.data, 'id_message': id_message - 10})


class CityCreate(CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
