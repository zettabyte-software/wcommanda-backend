from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, CadastroViewSet, LoginView

router_auth = DefaultRouter()
router_auth.register("", AuthViewSet, "auth")
router_auth.register("cadastro", CadastroViewSet, "cadastro")
# router_auth.register("login", LoginViewSet, "login")

urlpatterns = [
    path("auth/", include(router_auth.urls)),
    path("auth/login/", LoginView.as_view()),
]
