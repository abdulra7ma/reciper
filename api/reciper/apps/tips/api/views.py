from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from reciper.apps.tips.models import Tip, FavoriteTip
from .serializers import FavoriteTipSerializer
from .serializers import TipSerializer


@extend_schema(tags=["Tips"], responses={200: TipSerializer})
class TipListView(generics.ListCreateAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [permissions.AllowAny]  # Change as needed based on your security policy

    def get_permissions(self):
        if self.request.method == 'GET':
            return super().get_permissions()
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(tags=["Tips"], responses={200: TipSerializer})
class TipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as required

    def get_permissions(self):
        if self.request.method == 'GET':
            return super().get_permissions()
        return [permissions.IsAuthenticated()]


@extend_schema(tags=["Tips Favorites"], responses={200: FavoriteTipSerializer})
class AddFavoriteTipView(generics.CreateAPIView):
    queryset = FavoriteTip.objects.all()
    serializer_class = FavoriteTipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Tips Favorites"], responses={200: FavoriteTipSerializer})
class RemoveFavoriteTipView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        favorite_tip = FavoriteTip.objects.filter(id=pk, user=request.user)
        if favorite_tip.exists():
            favorite_tip.delete()
            return Response({"message": "Favorite tip removed"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Favorite tip not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Tips Favorites"], responses={200: FavoriteTipSerializer})
class ListFavoriteTipsView(generics.ListAPIView):
    serializer_class = FavoriteTipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteTip.objects.filter(user=self.request.user)
