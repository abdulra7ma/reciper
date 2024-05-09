from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reciper.apps.shopping.models import ShoppingList, ShoppingListItem
from .serializers import ShoppingListSerializer, ShoppingListItemSerializer


@extend_schema(tags=["Shopping Lists"], responses={status.HTTP_200_OK: ShoppingListSerializer})
class ShoppingListView(generics.ListCreateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Shopping Lists"], responses={status.HTTP_200_OK: ShoppingListSerializer})
class ShoppingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Shopping Lists"], responses={status.HTTP_200_OK: ShoppingListSerializer})
class ShoppingListItemView(generics.ListCreateAPIView):
    serializer_class = ShoppingListItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        shopping_list_id = self.kwargs.get('shopping_list_id')
        return ShoppingListItem.objects.filter(shopping_list_id=shopping_list_id)

    def perform_create(self, serializer):
        shopping_list_id = self.kwargs.get('shopping_list_id')
        serializer.save(shopping_list_id=shopping_list_id)


@extend_schema(tags=["Shopping Lists - Items"], responses={status.HTTP_200_OK: ShoppingListSerializer})
class PurchaseItemAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            item = ShoppingListItem.objects.get(id=item_id, shopping_list__user=request.user)
            item.is_purchased = True
            item.save()
            return Response({"status": "Item marked as purchased"}, status=status.HTTP_200_OK)
        except ShoppingListItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Shopping Lists - Items"], responses={status.HTTP_200_OK: ShoppingListSerializer})
class UnpurchaseItemAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            item = ShoppingListItem.objects.get(id=item_id, shopping_list__user=request.user)
            item.is_purchased = False
            item.save()
            return Response({"status": "Item marked as unpurchased"}, status=status.HTTP_200_OK)
        except ShoppingListItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
