from django.apps import AppConfig

from common.internal.checks.api.envs import check_required_env_vars  # noqa: F401


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.system.core"
