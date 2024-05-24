from django.contrib import admin
from .models import Podcast, ViewModel


# Register your models here.
@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    pass


@admin.register(ViewModel)
class ViewModelAdmin(admin.ModelAdmin):
    pass
