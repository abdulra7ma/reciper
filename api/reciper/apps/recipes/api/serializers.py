from rest_framework import serializers

from reciper.apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from reciper.apps.common.api.serializers import FileSerializer
from reciper.apps.recipes.models import Ingredient, RecipeIngredient, Recipe, Like, Comment, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'image']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient', write_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'ingredient_id', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, source='ingredients_set', write_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'description', 'time_required', 'difficulty_level', 'category', 'image',
                  'ingredients']
        read_only_fields = ['user']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_set')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients_set')
        ingredients = RecipeIngredient.objects.filter(recipe=instance)
        ingredients.delete()
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=instance, **ingredient_data)
        return super().update(instance, validated_data)


class RecipeListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    category = CategorySerializer()
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')
    image = FileSerializer()

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'description', 'time_required', 'difficulty_level', 'category', 'image',
                  'ingredients']


class RecipeHomeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    category = CategorySerializer()
    ingredients_list = RecipeIngredientSerializer(many=True, source='ingredients')
    image = FileSerializer()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'description', 'time_required', 'difficulty_level', 'category', 'image',
                  'ingredients_list', 'likes_count', 'comments_count', 'comments']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'recipe', 'user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'user', 'text', 'created_at']
        read_only_fields = ['recipe', 'user']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
