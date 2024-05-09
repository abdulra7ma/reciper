from django.urls import path

from .views import (
    ShoppingListView,
    ShoppingListDetailView,
    ShoppingListItemView,
    PurchaseItemAPIView,
    UnpurchaseItemAPIView
)

urlpatterns = [
    # URL for listing all shopping lists and creating a new shopping list
    path('', ShoppingListView.as_view(), name='shopping-lists'),

    # URL for retrieving, updating, and deleting a specific shopping list
    path('<int:pk>/', ShoppingListDetailView.as_view(), name='shopping-list-detail'),

    # URL for listing items in a specific shopping list and adding new items to it
    path('<int:shopping_list_id>/items/', ShoppingListItemView.as_view(), name='shopping-list-items'),

    # URL for marking an item as purchased
    path('items/<int:item_id>/purchase/', PurchaseItemAPIView.as_view(), name='purchase-item'),

    # URL for marking an item as unpurchased
    path('items/<int:item_id>/unpurchase/', UnpurchaseItemAPIView.as_view(), name='unpurchase-item'),
]
