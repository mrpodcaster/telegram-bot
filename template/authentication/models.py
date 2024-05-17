from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class TemplateUser(AbstractUser):
    telegram_id = models.CharField(null=True, blank=True, max_length=200)
