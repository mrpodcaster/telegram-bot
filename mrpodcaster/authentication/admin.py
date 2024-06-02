from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from mrpodcaster.api.models import PodcastView
from mrpodcaster.authentication.models import TelegramUser

class PodcastViewInline(admin.TabularInline):
    model = PodcastView
    extra = 0


# Register your models here
@admin.register(TelegramUser)
class TelegramUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "telegram_id")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    inlines = (PodcastViewInline,)
