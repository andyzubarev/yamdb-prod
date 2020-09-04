from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_confirmation_code, get_jwt_token, \
    CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/email/', get_confirmation_code),
    path('auth/token/', get_jwt_token),
]
