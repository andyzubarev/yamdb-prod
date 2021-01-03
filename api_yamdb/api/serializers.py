from rest_framework import serializers

from .models import User, Category, Genre, Title, Review, Comment


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя"""
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
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = GenreField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    def validate(self, attrs):
        request = self.context['request']
        if request.method != 'POST':
            return attrs

        title = Title.objects.filter(
            pk=self.context['view'].kwargs.get('title')).exists()
        if not title:
            return attrs

        title = Title.objects.get(pk=self.context['view'].kwargs.get('title'))
        review = Review.objects.filter(
            author=request.user).filter(title=title).exists()
        if review:
            raise serializers.ValidationError(
                  'One user can make only one review per title.')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id',  'review_id', 'text', 'author', 'pub_date')
