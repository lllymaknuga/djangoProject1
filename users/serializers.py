import requests

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError

from users.models import CustomUser, OtpToken


class CustomUserSerializer(ModelSerializer):
    class Meta:
        fields = ['phone_number']
        model = CustomUser


class OtpTokenGenerateSerializer(ModelSerializer):
    class Meta:
        fields = ['phone_number', 'check_id', 'call_phone']
        read_only_fields = ['check_id', 'call_phone']
        model = OtpToken

    def validate(self, attrs):
        if len(attrs['phone_number']) != 12:
            raise ValidationError('Введен номер неправильно')
        return attrs

    def create(self, validated_data):
        phone = validated_data['phone_number']

        url = f'https://sms.ru/callcheck/add?api_id=33A6FC6D-FA74-8486-346B-4727B7EFA8B3&phone={phone[1:]}&json=1'
        data = requests.post(url).json()
        check_id = data['check_id']
        call_phone = data['call_phone']
        if OtpToken.objects.filter(phone_number=phone).count() == 0:
            token = OtpToken.objects.create(phone_number=phone, check_id=check_id, call_phone=call_phone)
        else:
            token = OtpToken.objects.get(phone_number=phone)
            token.check_id = check_id
            token.save()
        return token


class OtpTokenValidateSerializer(ModelSerializer):
    class Meta:
        fields = ['phone_number']
        model = OtpToken

    def validate(self, attrs):
        phone = attrs['phone_number']
        if not OtpToken.objects.filter(phone_number=phone):
            raise ValidationError('Вы не прошли генерацию')
        check_id = OtpToken.objects.get(phone_number=phone).check_id
        url = f'https://sms.ru/callcheck/status?api_id=33A6FC6D-FA74-8486-346B-4727B7EFA8B3&check_id={check_id}&json=1'
        data = requests.get(url).json()
        if data['check_status'] == 402:
            raise ValidationError(data['check_status_text'])
        if data['check_status'] == 400:
            raise ValidationError(data['check_status_text'])
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
