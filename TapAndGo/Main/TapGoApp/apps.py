from django.apps import AppConfig


class TapgoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TapGoApp'

    def ready(self):
        import TapGoApp.signals
