from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

apps_urls = [path("api/", include(app + ".urls")) for app in settings.WCOMMANDA_APPS]

urlpatterns = [
    path("admin/", admin.site.urls),
    *apps_urls,
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
