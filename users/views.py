from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.authtoken.models import Token
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
        try:
            if serializer.is_valid(raise_exception=True):
                user = CustomUser.objects.get(phone_number=request.data['phone_number'])
                user.is_active = True
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                print(created)
                return Response({'token': token.key, 'username': user.username, 'user-id': user.id},
                                status=status.HTTP_201_CREATED)
        except:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                print(user)
                token, created = Token.objects.get_or_create(user=user)
                print(created)
                return Response({'token': token.key, 'username': user.username, 'user-id': user.id},
                                status=status.HTTP_201_CREATED)


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


class DeleteUser(UpdateAPIView):
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        token = Token.objects.get(key=request.headers['Authorization'].split(' ')[1])
        user = token.user
        token.delete()
        try:
            user.is_active = False
            user.save()
            return Response('Успешно удалено', status=status.HTTP_204_NO_CONTENT)
        except:
            return Response('Ошибка', status=status.HTTP_400_BAD_REQUEST)
