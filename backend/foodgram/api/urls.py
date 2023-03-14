from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserListView, IngredientsListView,
                       RecipesListView, TagsListView)

urlpatterns = [

]

api_v1_router = DefaultRouter()
api_v1_router.register(r'users', CustomUserListView)
api_v1_router.register(r'recipes', RecipesListView, basename='recipes')
api_v1_router.register(
    'ingredients',
    IngredientsListView,
    basename='ingredients'
)
api_v1_router.register('tags', TagsListView, basename='tags')

urlpatterns += [
    path('', include(api_v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
