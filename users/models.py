from functools import partial
from random import randint

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from djangoProject1 import settings


class CustomUser(AbstractUser):
    password = models.CharField(max_length=128, blank=True)
    phone_number = models.CharField(max_length=12, unique=True, blank=False)
    first_name = None
    last_name = None
    complains = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     self.username = 'Пользователь' + str(CustomUser.objects.count() + 1)
    #     super().save(*args, **kwargs)

    # status = models.ForeignKey('Status', on_delete=models.PROTECT, null=True, default=1)


# class Status(models.Model):
#     category = models.CharField(max_length=30, db_index=True, default=1)
#
#     def __str__(self):
#         return self.category


def get_partial_random_otp_code(start, end):
    return partial(randint, start, end)


class OtpToken(models.Model):
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    data_send = models.DateTimeField(_('date joined'), default=timezone.now)
    otp_code = models.IntegerField(default=get_partial_random_otp_code(1000, 10000))
    attempts = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


@receiver(post_save, sender=CustomUser)
def fok(sender, instance, created, **kwargs):
    if created:
        instance.username = 'Пользователь' + str(instance.id)
        instance.save()
