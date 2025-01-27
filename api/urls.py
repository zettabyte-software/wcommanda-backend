from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.system.core.handlers import custom_404_handler

apps_urls = [path("api/", include(app + ".urls")) for app in settings.WCOMMANDA_APPS]

if settings.IN_PRODUCTION:
    handler404 = custom_404_handler


urlpatterns = [
    path("admin/", admin.site.urls),
    *apps_urls,
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
