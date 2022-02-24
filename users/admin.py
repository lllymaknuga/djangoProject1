from django.contrib import admin
from users.models import CustomUser, OtpToken

admin.site.register(CustomUser)
admin.site.register(OtpToken)