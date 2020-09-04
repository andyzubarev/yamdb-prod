from rest_framework import serializers

from .models import User


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