from django.conf import settings
from django.db.models import ProtectedError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from django_multitenant.utils import get_current_tenant
from threadlocals.threadlocals import get_request_variable


class BaseViewSet(GenericViewSet):
    serializer_classes = {}
    serializer_class = None
    filterset_fields = {}
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        distinct_fields = self.request.query_params.get("distinct", None)
        if distinct_fields is not None:
            return queryset.distinct(*distinct_fields)
        return queryset.filter(ambiente=get_current_tenant())

    def get_serializer_class(self):
        assert self.serializer_classes != {} or self.serializer_class is not None, (
            f"'{self.__class__.__name__}' deve implementar o 'serializer_class' ou  'serializer_classes'."
        )

        if self.serializer_class:
            return self.serializer_class

        return self.serializer_classes[self.action]

    def get_aditional_serializer_context(self):
        return {}

    def get_serializer_context(self):
        context = super().get_serializer_context()
        aditional_context = self.get_aditional_serializer_context()
        return {"action": self.action, "token": get_request_variable("token"), **context, **aditional_context}

    def get_host(self):
        if settings.IN_DEVELOPMENT:
            return "zettabyte.wcommanda.com.br"
        return self.request.get_host()

    def get_subdominio(self):
        return self.get_host().split(".")[0]

    def generic_action(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = kwargs.get("status", status.HTTP_200_OK)
        response_data = kwargs.get("data", None)
        return Response(response_data, status=response_status)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class BaseModelViewSet(BaseViewSet, ModelViewSet):
    tenant_view = True
    model = None
    serializer_classes = {}
    serializer_class = None
    filterset_fields = {}
    search_fields = []
    ordering_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()

        fields = self.request.query_params.get("fields", None)

        if fields is not None:
            queryset = queryset.values(*fields)

        distinct_fields = self.request.query_params.get("distinct", None)
        if distinct_fields is not None:
            queryset = queryset.distinct(*distinct_fields).order_by(*distinct_fields)
            if self.tenant_view:
                queryset = queryset.filter(ambiente=get_current_tenant())
            return queryset

        if self.tenant_view:
            queryset = queryset.filter(ambiente=get_current_tenant())

        return queryset

    def get_serializer_class(self):
        assert self.serializer_classes != {} or self.serializer_class is not None, (
            f"'{self.__class__.__name__}' deve implementar o 'serializer_class' ou  'serializer_classes'."
        )

        if self.serializer_class:
            return self.serializer_class

        return self.serializer_classes[self.action]

    def get_object(self):
        instance = super().get_object()
        self.instance = instance
        return instance

    def get_aditional_serializer_context(self):
        return {}

    def get_serializer_context(self):
        context = super().get_serializer_context()
        aditional_context = self.get_aditional_serializer_context()
        return {"action": self.action, "token": get_request_variable("token"), **context, **aditional_context}

    def get_host(self):
        if settings.IN_DEVELOPMENT:
            return "zettabyte.wcommanda.com.br"
        return self.request.get_host()

    def get_subdominio(self):
        return self.get_host().split(".")[0]

    def perform_create(self, serializer, **overwrite):
        return serializer.save(owner=self.request.user, **overwrite)

    def perform_update(self, serializer, **overwrite):
        return serializer.save(**overwrite)

    def alterar_campos_unicos(self, instance):
        """Alterar campos antes da clonagem."""

    def generic_action(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = kwargs.get("status", status.HTTP_200_OK)
        response_data = kwargs.get("data", None)
        return Response(response_data, status=response_status)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {"mensagem": "Esse registro já foi utilizado pelo sistema"},
                status=status.HTTP_409_CONFLICT,
            )

    @action(methods=["post"], detail=False)
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["get"], detail=True)
    def clonar(self, request, pk):
        instance = self.get_object()
        clone = instance.clonar()
        self.alterar_campos_unicos(clone)
        clone.save()
        serializer = self.get_serializer(clone)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def values(self, request):
        values = request.query_params.get("values", None)
        if values is None:
            return Response({"values": "Essa query é obrigatória"}, status=status.HTTP_400_BAD_REQUEST)

        values = values.split(",")
        queryset = self.filter_queryset(self.get_queryset()).values(*values)
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(page)

