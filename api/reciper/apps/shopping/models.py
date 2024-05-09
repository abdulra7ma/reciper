from django.db import models


class ShoppingList(models.Model):
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='shopping_lists')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    ingredient = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient} [{self.is_purchased}]"
