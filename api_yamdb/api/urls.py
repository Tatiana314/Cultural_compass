from api.views import (CategorieViewSet, CommentViewSet, GenreViewset,
                       ObtainJWTView, ReviewViewSet, TitleViewSet, UserViewSet,
                       user_signup_view)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'
VERSION = 'v1'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register('categories', CategorieViewSet, basename='categories')
router.register('genres', GenreViewset, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='titles'
)


urlpatterns = [
    path(f'{VERSION}/auth/token/', ObtainJWTView.as_view(), name='token'),
    path(f'{VERSION}/auth/signup/', user_signup_view, name='signup'),
    path(f'{VERSION}/', include(router.urls)),
]
