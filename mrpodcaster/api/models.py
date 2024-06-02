from django.db import models
from django.db.models import UniqueConstraint


class DifficultyLevel(models.TextChoices):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "challenging"


class Podcast(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="podcasts", null=False)
    difficulty = models.CharField(choices=DifficultyLevel.choices, max_length=12)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PodcastView(models.Model):
    podcast = models.ForeignKey("api.Podcast", on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.TelegramUser", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "podcast"], name="unique_podcast_view"),
        ]

    def __str__(self):
        return f'{self.podcast} - {self.user}: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
