from django.apps import AppConfig


class HomeservicesConfig(AppConfig):
    name = 'HomeServices'
    default_auto_field = 'django.db.models.BigAutoField'
    def ready(self):
        import HomeServices.signals

