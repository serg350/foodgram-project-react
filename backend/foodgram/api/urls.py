from django.urls import include, path
from rest_framework.routers import DefaultRouter


from api.views import RecipesListView, IngredientsListView, TagsListView

api_v1_router = DefaultRouter()
api_v1_router.register('recipes', RecipesListView, basename='recipes')
api_v1_router.register('ingredients', IngredientsListView, basename='ingredients')
api_v1_router.register('tags', TagsListView, basename='tags')

urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
