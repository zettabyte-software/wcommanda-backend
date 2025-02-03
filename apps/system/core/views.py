from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class ImTeapootViewSet(ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def list(self, request):
        return Response(status=status.HTTP_418_IM_A_TEAPOT)

    def retrieve(self, request):
        return Response(status=status.HTTP_418_IM_A_TEAPOT)

    def create(self, request):
        return Response(status=status.HTTP_418_IM_A_TEAPOT)

    def partial_update(self, request):
        return Response(status=status.HTTP_418_IM_A_TEAPOT)

    def update(self, request):
        return Response(status=status.HTTP_418_IM_A_TEAPOT)

    def destroy(self, request):
        return Response(status=status.HTTP_418_IM_A_TEAPOT)

