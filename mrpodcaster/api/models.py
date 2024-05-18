# Create your models here.
from django.db import models


class Podcast(models.Model):
    audio_file = models.FileField(upload_to="audio", null=False)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
