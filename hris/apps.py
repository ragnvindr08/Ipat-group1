from django.apps import AppConfig


class HrisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hris'
    def ready(self):
        import hris.signals
