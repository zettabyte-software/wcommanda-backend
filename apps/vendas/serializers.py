from rest_framework import serializers


class DashboardQueryParamSerializer(serializers.Serializer):
    data_inicio = serializers.DateField(error_messages={"required": "Essa query é obrigatória"})
    data_fim = serializers.DateField(error_messages={"required": "Essa query é obrigatória"})
