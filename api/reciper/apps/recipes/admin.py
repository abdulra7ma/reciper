from django.contrib import admin

from reciper.apps.recipes.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ...
