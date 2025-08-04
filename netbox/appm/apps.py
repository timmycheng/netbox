from django.apps import AppConfig


class APPMConfig(AppConfig):
    name = "appm"
    verbose_name = "APPM"

    def ready(self):
        from netbox.models.features import register_models
        from . import signals, search  # noqa: F401

        # Register models
        register_models(*self.get_models())