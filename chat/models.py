from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    city_id = models.ForeignKey('City', on_delete=models.PROTECT, null=True)