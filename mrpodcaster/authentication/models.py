from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class DifficultyLevel(models.TextChoices):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "challenging"


class TelegramUser(AbstractUser):
    telegram_id = models.CharField(null=True, blank=True, max_length=255)
    level = models.CharField()
