from rest_framework import serializers

from ingredients.models import Ingredients
from recipes.models import Recipes
from tags.models import Tags


class IngredientsSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredients


class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tags


class RecipesSerializers(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Tags.objects.all(),
        many=True
    )

    ingredients = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=IngredientsSerializers,
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Recipes

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tags'] = TagsSerializers(instance.tags, many=True).data
        response['ingredients'] = IngredientsSerializers(instance.ingredients, many=True).data
        return response
