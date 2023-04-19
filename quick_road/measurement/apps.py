from django.apps import AppConfig


class MeasurementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'measurement'
    verbose_name = 'measurements between 2 locations'