from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class TelegramUser(AbstractUser):
    telegram_id = models.CharField(null=True, blank=True, max_length=255)
    viewed_podcasts = models.ManyToManyField("api.Podcast", through="api.PodcastView")

    def __str__(self):
        return f"{self.username} - {self.telegram_id}"
