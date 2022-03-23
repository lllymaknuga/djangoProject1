from django.contrib import admin

from chat.models import City, Message


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ['id', 'name']


admin.site.register(City, CityAdmin)


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['id', 'content', 'city_id', 'created_at']


admin.site.register(Message, MessageAdmin)
