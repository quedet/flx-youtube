from django.apps import AppConfig


class ChannelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.channel'

    def ready(self):
        from apps.channel import receivers