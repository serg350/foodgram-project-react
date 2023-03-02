from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from api.serilizers import RecipesSerializers, IngredientsSerializers, TagsSerializers, CustomUserSerializer, \
    RecipesWriteSerializer, CustomUserCreateSerializer
from ingredients.models import Ingredients
from recipes.models import Recipes
from tags.models import Tags
from users.models import User


class CustomUserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    #serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CustomUserSerializer
        return CustomUserCreateSerializer


class RecipesListView(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    #serializer_class = RecipesSerializers

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSerializers
        return RecipesWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientsListView(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializers


class TagsListView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializers
