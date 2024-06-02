# Register your models here.
from django.contrib import admin

from mrpodcaster.api import models


@admin.register(models.Podcast)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'difficulty', 'updated_at', 'archived')
    list_filter = ('difficulty',)
    search_fields = ('title', 'description')

    date_hierarchy = 'updated_at'

