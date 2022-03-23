from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import CustomUserSerializer, OtpTokenGenerateSerializer, OtpTokenValidateSerializer, \
    CustomUsernameSerializer


class CustomUserCreateView(CreateAPIView):
    serializer_class = CustomUserSerializer


class CustomUserViewList(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class PhonNumberOtpCodeGenerate(CreateAPIView):
    serializer_class = OtpTokenGenerateSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        return self.create(request, *args, **kwargs)


class PhonNumberOtpCodeValidate(CreateAPIView):
    serializer_class = OtpTokenValidateSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            print(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)


class UpdateUsername(UpdateAPIView):
    serializer_class = CustomUsernameSerializer

    def update(self, request, *args, **kwargs):
        print(request.data)
        print(request.headers['Authorization'].split(' ')[1])
        user = Token.objects.get(key=request.headers['Authorization'].split(' ')[1]).user
        print(user)
        username = request.data['username']
        try:
            user.username = username
            user.save()
            return Response(f'username изменился на {username}', status=status.HTTP_200_OK)
        except:
            return Response('Ошибка', status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(DestroyAPIView):
    serializer_class = CustomUserSerializer

    def delete(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.headers['Authorization'].split(' ')[1]).user
        print(user)
        try:
            user.delete()
            return Response('Успешно удалено', status=status.HTTP_204_NO_CONTENT)
        except:
            return Response('Ошибка', status=status.HTTP_400_BAD_REQUEST)
