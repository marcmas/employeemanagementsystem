from django.apps import AppConfig


class EmsConfig(AppConfig):
    name = 'ems'

    def ready(self):
        import leave.signals