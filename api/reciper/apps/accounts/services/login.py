from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reciper.apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer


class LoginService:
    @classmethod
    def login(cls, request, user):
        refresh = RefreshToken.for_user(user)
        return Response(data={
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserProfileSerializer(user).data,
        }, status=status.HTTP_200_OK)

    @classmethod
    def logout(cls, request):
        cls._django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _django_logout(request):  # pragma: no cover
        django_logout(request)

    @staticmethod
    def _django_login(request, user):  # pragma: no cover
        django_login(request, user)
