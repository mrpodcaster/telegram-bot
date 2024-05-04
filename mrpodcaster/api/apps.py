from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mrpodcaster.api"

    def ready(self):
        if settings.BOT_MAIN:
            from django_asgi_lifespan.register import register_lifespan_manager
            from mrpodcaster.api.telegram.bot import bot_lifespan

            register_lifespan_manager(
                context_manager=bot_lifespan,
            )
