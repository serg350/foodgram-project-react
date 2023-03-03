from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from djoser.serializers import UserCreateSerializer, UserSerializer

from ingredients.models import Ingredients
from recipes.models import Recipes, Favorite, ShoppingCart, RecipesIngredient
from tags.models import Tags
from users.models import Follower

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = 'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed'
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


#class PasswordSerializers(serializers.ModelSerializer):
#    model = User
#
#    old_password = serializers.CharField(required=True)
#    new_password = serializers.CharField(required=True)


class FollowSerializers(serializers.ModelSerializer):
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Follower

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Follower.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

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

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError({
                'ingredients': 'Нужен хотя бы один ингредиент!'
            })
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredients, id=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError({
                    'ingredients': 'Ингридиенты не могут повторяться!'
                })
            if int(item['amount']) <= 0:
                raise ValidationError({
                    'amount': 'Количество ингредиента должно быть больше 0!'
                })
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError({
                'tags': 'Нужно выбрать хотя бы один тег!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({
                    'tags': 'Теги должны быть уникальными!'
                })
            tags_list.append(tag)
        return value

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
