from api.filters import TitleFilter
from api.permissions import (AdminOnlyPermission, IsAdminOrReadOnly,
                             IsAuthorUser, IsModeratorUser)
from api.serializers import (CategorieSerializer, CommentSerializer,
                             GenreSerializer, ObtainJWTSerializer,
                             ReviewSerializer, TitleGetSerializer,
                             TitleSerializer, UserMeSerializer, UserSerializer,
                             UserSignUpSerializer)
from api.viewsets import GetCreateDelete
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categorie, Genre, Review, Title
from users.models import User


class ReviewViewSet(viewsets.ModelViewSet):
    """Получаем/создаем/удаляем/редактируем отзывы."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly | IsAuthorUser | IsModeratorUser
    )

    def title_object(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.title_object().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_object())


class CommentViewSet(viewsets.ModelViewSet):
    """Получаем/создаем/удаляем/редактируем комментарии."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly | IsAuthorUser | IsModeratorUser
    )

    def get_queryset(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        ).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=get_object_or_404(
                Review,
                title_id=self.kwargs['title_id'],
                id=self.kwargs['review_id'],
            ),
            author=self.request.user,
        )


class CategorieViewSet(GetCreateDelete):
    """Получаем/создаем/удаляем категорию."""

    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewset(GetCreateDelete):
    """Получаем/создаем/удаляем жанр."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получаем/создаем/удаляем/редактируем произведение."""

    queryset = (
        Title.objects.prefetch_related('reviews')
        .annotate(rating=Avg('reviews__score'))
        .order_by('name')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup_view(request):
    """Регистрация пользователя"""
    username = request.data.get('username')
    email = request.data.get('email')

    user = User.objects.filter(email=email, username=username).first()
    if user is not None:
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=email, confirmation_code=confirmation_code
        )
        return Response(
            {'Оповещение': 'Письмо с кодом отправлено на маил'},
            status=status.HTTP_200_OK,
        )
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    user = User.objects.create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_confirmation_code(email=email, confirmation_code=confirmation_code)

    return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """User CRUD"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnlyPermission]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        serializer_class=UserMeSerializer,
    )
    def me(self, request):
        """Обрабатывает GET запрос users/me"""
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def patch_me(self, request):
        """Обрабатывает PATCH запрос users/me"""
        user = request.user
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainJWTView(APIView):
    """Отправляет JWT токен в ответ на ПОСТ запрос с кодом"""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ObtainJWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})


def send_confirmation_code(email, confirmation_code):
    """Отправляем email сообщение пользователю с его кодом"""
    subject = 'Код подтверждения'
    message = f'Код подтверждения для регистрации: {confirmation_code}'
    from_email = 'sredawork26@gmail.com'
    recipient_list = [email]
    fail_silently = True

    send_mail(subject, message, from_email, recipient_list, fail_silently)
