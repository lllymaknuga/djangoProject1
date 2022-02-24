from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import CustomUserSerializer, OtpTokenGenerateSerializer, OtpTokenValidateSerializer


class CustomUserCreateView(CreateAPIView):
    serializer_class = CustomUserSerializer


class CustomUserViewList(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class PhonNumberOtpCodeGenerate(CreateAPIView):
    serializer_class = OtpTokenGenerateSerializer


class PhonNumberOtpCodeValidate(CreateAPIView):
    serializer_class = OtpTokenValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
