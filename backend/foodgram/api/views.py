from django.shortcuts import render
from rest_framework import viewsets

from api.serilizers import RecipesSerializers, IngredientsSerializers, TagsSerializers
from ingredients.models import Ingredients
from recipes.models import Recipes
from tags.models import Tags


class RecipesListView(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializers


class IngredientsListView(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializers


class TagsListView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializers
