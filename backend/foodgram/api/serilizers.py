from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import SerializerMethodField
from djoser.serializers import UserCreateSerializer, UserSerializer

from ingredients.models import Ingredients
from recipes.models import Recipes, Favorite, ShoppingCart, RecipesIngredient
from tags.models import Tags
from users.models import User, Follower


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = 'email', 'id', 'first_name', 'last_name', 'is_subscribed'
        model = User

    def get_is_subscribed(self, obj):
        return (
                self.context.get('request').user.is_authenticated
                and Follower.objects.filter(user=self.context['request'].user,
                                            author=obj).exists()
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """[POST] Создание нового пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate(self, obj):
        invalid_usernames = ['me', 'set_password',
                             'subscriptions', 'subscribe']
        if self.initial_data.get('username') in invalid_usernames:
            raise serializers.ValidationError(
                {'username': 'Вы не можете использовать этот username.'}
            )
        return obj



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
        slug_field='pk',
        queryset=Tags.objects.all(),
        many=True
    )

    # ingredients = serializers.SlugRelatedField(
    #    slug_field='name',
    #    read_only=True,
    #    default=IngredientsSerializers,
    #    many=True
    # )
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = '__all__'
        model = Recipes

    def get_is_favorited(self, obj):
        return (
                self.context.get('request').user.is_authenticated
                and Favorite.objects.filter(user=self.context['request'].user,
                                            recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
                self.context.get('request').user.is_authenticated
                and ShoppingCart.objects.filter(
            user=self.context['request'].user,
            recipe=obj).exists()
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipesingredient__amount')
        )
        return ingredients

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tags'] = TagsSerializers(instance.tags, many=True).data
        # response['ingredients'] = IngredientsSerializers(instance.ingredients, many=True).data
        return response


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipesIngredient
        fields = ('id', 'amount')


class RecipesWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)

    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    @transaction.atomic
    def create_ingredients_amounts(self, ingredients, recipe):
        RecipesIngredient.objects.bulk_create(
            [RecipesIngredient(
                ingredient=Ingredients.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amounts(recipe=recipe,
                                        ingredients=ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amounts(recipe=instance,
                                        ingredients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipesSerializers(instance,
                                  context=context).data


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribeSerializer(CustomUserSerializer):
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes_count', 'recipes'
        )
        read_only_fields = ('email', 'username')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
        return serializer.data
