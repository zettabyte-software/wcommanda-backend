from django.http import JsonResponse


def custom_404_handler(request, exception):
    return JsonResponse({"mensagem": "Endpoint não encontrado"})
