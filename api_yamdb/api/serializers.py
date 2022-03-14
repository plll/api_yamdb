import re
import datetime as dt
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, User, Genre, Category, Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Может существовать только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username']

    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                "Нельзя создавать пользователя ME"
            )
        if value == '':
            raise serializers.ValidationError("Нужно заполнить имя")
        return value

    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError("Нужно заполнить почту")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class ValidateSlugNameSerializer(serializers.ModelSerializer):
    def validate_slug(self, value):
        if (
            re.match('^[-a-zA-Z0-9_]+$', value) is not None and len(value) < 51
        ):
            return value
        raise serializers.ValidationError(
            "Slug должен состоять из латинских букв и не длиннее 50 символов"
        )

    def validate_name(self, value):
        if len(value) < 257:
            return value
        raise serializers.ValidationError(
            "Длина имени не должна превышать 256 символов"
        )


class GenreSerializer(ValidateSlugNameSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(ValidateSlugNameSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlesPostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if dt.date.today().year < value and value > 0:
            raise serializers.ValidationError(
                'Неправильно указан год'
            )
        return value


class TitlesGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta():
        fields = '__all__'
        read_only_fields = ('id',)
        model = Title


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'bio', 'email',
            'first_name', 'last_name', 'role'
        )


class UsersMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'bio', 'email',
            'first_name', 'last_name', 'role'
        )
        read_only_fields = ('role',)
