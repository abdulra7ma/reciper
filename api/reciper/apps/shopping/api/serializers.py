from rest_framework import serializers

from reciper.apps.shopping.models import ShoppingList, ShoppingListItem


class ShoppingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItem
        fields = ['id', 'ingredient', 'quantity', 'is_purchased']


class ShoppingListSerializer(serializers.ModelSerializer):
    items = ShoppingListItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingList
        fields = ['id', 'user', 'title', 'created_at', 'updated_at', 'items']
        read_only_fields = ['user']
