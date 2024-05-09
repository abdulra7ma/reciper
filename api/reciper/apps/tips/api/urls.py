from django.urls import path

from .views import TipListView, TipDetailView, RemoveFavoriteTipView, AddFavoriteTipView, ListFavoriteTipsView

urlpatterns = [
    path('', TipListView.as_view(), name='tips-list'),
    path('<int:pk>/', TipDetailView.as_view(), name='tip-detail'),
    path('favorite-tips/add/', AddFavoriteTipView.as_view(), name='add-favorite-tip'),
    path('favorite-tips/remove/<int:pk>/', RemoveFavoriteTipView.as_view(), name='remove-favorite-tip'),
    path('favorite-tips/', ListFavoriteTipsView.as_view(), name='list-favorite-tips'),
]
