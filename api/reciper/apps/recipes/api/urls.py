from django.urls import path

from .views import RecipeListCreateAPIView, RecipeRetrieveUpdateDestroyAPIView, RecipeListByUserAPIView, \
    RecentRecipesAPIView, LikeRecipeAPIView, RecipeLikesCountAPIView, RecipeCommentsAPIView, RecipesByCategoryAPIView, \
    UnlikeRecipeAPIView

urlpatterns = [
    path('recipes/', RecipeListCreateAPIView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeRetrieveUpdateDestroyAPIView.as_view(), name='recipe-detail'),
    path('users/<int:user_id>/recipes/', RecipeListByUserAPIView.as_view(), name='user-recipes'),
    path('recipes/home/', RecentRecipesAPIView.as_view(), name='home-recipes'),
    path('recipes/<int:pk>/like/', LikeRecipeAPIView.as_view(), name='like-recipe'),
    path('recipes/<int:pk>/unlike/', UnlikeRecipeAPIView.as_view(), name='unlike-recipe'),
    path('recipes/<int:pk>/likes/count/', RecipeLikesCountAPIView.as_view(), name='recipe-likes-count'),
    path('recipes/<int:pk>/comments/', RecipeCommentsAPIView.as_view(), name='recipe-comments'),
    path('recipes/category/<int:category_id>/', RecipesByCategoryAPIView.as_view(), name='recipes-by-category'),
]
