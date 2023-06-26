from django.apps import AppConfig


class BaseModuleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "base_module"
