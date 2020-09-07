from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, \
    IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitlesFilter
from .models import User, Category, Genre, Title, Review, Comment
from .permissions import IsAdminOrSuperUser, \
    IsAdminOrReadOnly, \
    ReviewCommentPermissions
from .serializers import ConfirmationCodeSerializer, \
    UserEmailSerializer, UserSerializer, \
    CategorySerializer, GenreSerializer, \
    TitleSerializer, ReviewSerializer, CommentSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    '''API для отправки кода подтверждения на почту'''
    username = request.data.get('username')
    serializer = UserEmailSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email')
    if username is not None:
        try:
            User.objects.create_user(username=username, email=email)
        except IntegrityError:
            return Response(
                {'Error': 'Пользователь с таким '
                          'username/email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
                )
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    mail_subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    send_mail(mail_subject, message, 'Yamdb.ru <admin@yamdb.ru>',
              [email], fail_silently=False)
    return Response(
        {'Успешно': f'На почту {email} был выслан код подтверждения'},
        status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    '''API для получения jwt-токена'''
    serializer = ConfirmationCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)}, 
            status=status.HTTP_200_OK
            )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    '''API для модели пользователя'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrSuperUser]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        '''API для получения и редактирования
        текущим пользователем своих данных'''
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ReviewCommentPermissions, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ReviewCommentPermissions, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)

