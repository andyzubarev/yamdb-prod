from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, get_confirmation_code, get_jwt_token, 
CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register(
    r'titles/(?P<title>\d+)/reviews', ReviewViewSet, basename='reviews'
    )
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', 
    CommentViewSet, 
    basename='comments'
    )

v1_auth_patterns = [
    path('mail/', get_confirmation_code),
    path('token/', get_jwt_token)
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(v1_auth_patterns))
]

