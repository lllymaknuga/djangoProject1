from datetime import timedelta

from django.utils import timezone

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from rest_framework.authtoken.models import Token

from users.models import CustomUser, OtpToken


class CustomUserSerializer(ModelSerializer):
    class Meta:
        fields = ['phone_number', ]
        model = CustomUser


class OtpTokenGenerateSerializer(ModelSerializer):
    class Meta:
        fields = ['phone_number']
        model = OtpToken

    def validate(self, attrs):
        if OtpToken.objects.filter(phone_number=attrs['phone_number'], data_send__day=timezone.now().day).count() > 5:
            raise ValidationError('Число попыток закончилось(')
        return attrs


class OtpTokenValidateSerializer(ModelSerializer):
    class Meta:
        fields = ['phone_number', 'otp_code']
        model = OtpToken

    def validate(self, attrs):
        phone = attrs['phone_number']
        otp_code = attrs['otp_code']
        if not OtpToken.objects.filter(otp_code=otp_code, phone_number=phone).last():
            raise ValidationError('Что-то пошло не так. Получите код')
        if OtpToken.objects.filter(phone_number=phone).last().otp_code != otp_code:
            OtpToken.objects.filter(phone_number=phone).last().attempts += 1
            raise ValidationError('Попытки закончились. Получите код заново')
        if timezone.now() - OtpToken.objects.filter(phone_number=attrs['phone_number']).last().data_send > timedelta(
                minutes=3):
            raise ValidationError('Время жизни токена закончилось. Получите код заново')
        return attrs

    def create(self, validated_data):
        phone = validated_data['phone_number']
        user_serializer = CustomUserSerializer(data={'phone_number': phone})
        if not CustomUser.objects.filter(phone_number=phone):
            user_serializer.is_valid()
            user = user_serializer.save()
            return user
        user = CustomUser.objects.get(phone_number=phone)
        return user
