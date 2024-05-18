# Create your models here.

from django.db import models
from django.utils import timezone


class CreatedUpdatedDeletedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def perform_destroy(self, instance):
        if self.deleted_at is not None:
            self.delete()
            return

        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True


class Podcast(CreatedUpdatedDeletedAtMixin):
    audio_file = models.FileField(upload_to="audio", null=False)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)

    script = models.TextField(null=False)
    script_file = models.FileField(upload_to="script", null=False)

    archived = models.BooleanField(default=False)
