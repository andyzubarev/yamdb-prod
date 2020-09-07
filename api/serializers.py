from rest_framework import serializers

from .models import User, Category, Genre, Title, Review, Comment
from rest_framework.validators import UniqueTogetherValidator


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор модели пользователя'''
    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'role', 
            'email', 
            'first_name', 
            'last_name', 
            'bio'
            )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Category


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(slug_field='slug', queryset=Category.objects.all(), required=False)
    genre = GenreField(slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    title = serializers.ReadOnlyField(source='review.title')

    class Meta:
        model = Review
        fields = ('id', 'score', 'text', 'created', 'author', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'created')
        model = Comment
