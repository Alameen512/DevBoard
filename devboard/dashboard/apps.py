from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        # Connects the post_save signal that auto-creates a Profile
        # for every new User (see dashboard/signals.py).
        import dashboard.signals  # noqa: F401
