# Generated by Django 4.0.2 on 2022-02-24 11:19

from django.db import migrations, models
import functools
import random


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.IntegerField(default=functools.partial(random.Random.randint, *(1000, 10000), **{})),
        ),
    ]
