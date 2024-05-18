from django.contrib import admin
from .models import Podcast, TelegramConversationView


# Register your models here.
@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramConversationView)
class TelegramConversationViewAdmin(admin.ModelAdmin):
    pass