from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year_release


class Categorie(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Введите название категории',
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Метка')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Введите название жанра',
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Метка')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения (определённый фильм, книга или песенка)."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска', validators=[validate_year_release]
    )
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Categorie,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория, к которому относиться произведение',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        help_text='Жанры, к которым относиться произведение',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}, {self.year}, {self.category}, {self.genre}'


class GenreTitle(models.Model):
    """Модель связи id произведения и id жанра."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель для отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]

    def __str__(self):
        return (
            f"Отзыв от {self.author.username} на произведение '{self.title}'"
        )


class Comment(models.Model):
    """Модель для комментариев."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
