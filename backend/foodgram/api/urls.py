from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.serilizers import IngredientsSerializers
from api.views import RecipesListView, IngredientsListView

api_v1_router = DefaultRouter()
api_v1_router.register('recipes', RecipesListView, basename='recipes')
api_v1_router.register('ingredients', IngredientsListView, basename='ingredients')

urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
    #path('v1/auth/', include(auth_urls)),
]
