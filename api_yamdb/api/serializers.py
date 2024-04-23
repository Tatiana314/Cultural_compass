from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from reviews.models import Categorie, Comment, Genre, Review, Title
from reviews.validators import validate
from users.models import User


class ObtainJWTSerializer(serializers.Serializer):
    """Сериалайзер для получения токена пользователем"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        if not username or not confirmation_code:
            raise serializers.ValidationError(
                "Заполните все обязательные" "строки"
            )

        user = User.objects.filter(username=username)
        if not user.exists():
            raise NotFound("Неверный username")

        user = user.first()
        confirmation_code_chek = default_token_generator.check_token(
            user, token=confirmation_code
        )
        if not confirmation_code_chek:
            raise serializers.ValidationError("Неправильный код доступа")

        attrs['user'] = user
        return attrs


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        read_only_fields = ('id', 'role')

    def validate(self, data):
        validate(self, data)
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate(self, data):
        validate(self, data)
        return super().validate(data)


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        validate(self, data)
        return super().validate(data)


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorieSerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Categorie.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            title=self.context['view'].kwargs['title_id'],
            author=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data
