from django.apps import AppConfig


class ElectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elections'

    def ready(self):
        # Import the signal handlers to ensure they are registered
        import elections.signals
