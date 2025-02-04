from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reciper.apps.accounts.api.v1.serializers.password import (
    ChangePasswordSerializer,
    ConfirmResetPasswordSerializer,
    ResetPasswordSerializer,
)


class ChangePasswordAPIView(CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Change password", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()}
    )
    def post(self, request, *args, **kwargs):  # pragma: no cover
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordAPIView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    @extend_schema(
        summary="Reset password", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()}
    )
    def post(self, request, *args, **kwargs):  # pragma: no cover
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfirmResetPasswordAPIView(CreateAPIView):
    serializer_class = ConfirmResetPasswordSerializer

    @extend_schema(
        summary="Confirm reset password", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()}
    )
    def post(self, request, *args, **kwargs):  # pragma: no cover
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
