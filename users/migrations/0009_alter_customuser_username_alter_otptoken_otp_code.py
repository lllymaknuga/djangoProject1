# Generated by Django 4.0.2 on 2022-02-23 16:06

import django.contrib.auth.validators
from django.db import migrations, models
import functools
import random


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_username_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.IntegerField(default=functools.partial(random.Random.randint, *(1000, 10000), **{})),
        ),
    ]
