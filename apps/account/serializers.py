from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer, PasswordField
from rest_framework import serializers

from django.contrib.auth import authenticate


class AuthSerializer(TokenObtainSlidingSerializer):
    """
    Сериализатор для авторизации
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(max_length=150)
        self.fields["password"] = PasswordField()

    def validate(self, attrs):
        credentials = {
            'username': attrs.get("username"),
            'password': attrs.get("password")
        }

        user = authenticate(
            username=credentials['username'], password=credentials['password'])

        if user is None:
            raise serializers.ValidationError(
                {'message': 'Неверный логин или пароль'}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {'message': 'Ваша учетная запись не активна'}
            )

        return super().validate(credentials)
