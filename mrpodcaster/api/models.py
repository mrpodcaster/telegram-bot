from django.db import models
from ..authentication.models import TelegramUser
# Create your models here.


class Podcast(models.Model):
    name = models.CharField(max_length=200, default="Podcast")
    description = models.CharField(max_length=200, default="Podcast Description")
    podcastFile = models.FileField(upload_to="audio", default=None)


class ViewModel(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
