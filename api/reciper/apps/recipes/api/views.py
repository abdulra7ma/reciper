from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from .serializers import RecipeSerializer, CommentSerializer, RecipeHomeSerializer, LikeSerializer
from ..models import Recipe, Like, Comment


@extend_schema(tags=["Recipes"], responses={200: RecipeSerializer})
class RecipeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeSerializer
        return RecipeHomeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically assign the logged-in user as the recipe creator


@extend_schema(tags=["Recipes"], responses={200: RecipeSerializer})
class RecipeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)  # Ensure the user updating the recipe is the logged-in user


@extend_schema(tags=["Recipes By User"], responses={200: RecipeSerializer})
class RecipeListByUserAPIView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Recipe.objects.filter(user_id=user_id)


@extend_schema(tags=["Recipes Home"], responses={200: RecipeHomeSerializer})
class RecentRecipesAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all().order_by('-created_at')[:10]  # Adjust the number according to your requirements
    serializer_class = RecipeHomeSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["Likes"], responses={200: RecipeSerializer})
class LikeRecipeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(recipe=recipe, user=request.user)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_409_CONFLICT)

    def delete(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        Like.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Likes"], responses={200: LikeSerializer})
class UnlikeRecipeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        Like.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Comments"], responses={200: CommentSerializer})
class RecipeLikesCountAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        likes_count = Like.objects.filter(recipe_id=pk).count()
        return Response({"likes_count": likes_count})


@extend_schema(tags=["Comments"], responses={200: CommentSerializer})
class RecipeCommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_id = self.kwargs['pk']
        return Comment.objects.filter(recipe_id=recipe_id)

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, recipe=recipe)


@extend_schema(tags=["Recipes By Category"], responses={200: RecipeSerializer})
class RecipesByCategoryAPIView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]  # Update permissions as needed

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Recipe.objects.filter(category_id=category_id)
