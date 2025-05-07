from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from rest_framework import status


def custom_404_handler(request, exception):
    return JsonResponse({"mensagem": _("Endpoint não encontrado ainda")}, status=status.HTTP_404_NOT_FOUND)
