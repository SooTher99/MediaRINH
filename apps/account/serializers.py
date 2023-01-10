from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer, PasswordField
from rest_framework import serializers

from django.contrib.auth import authenticate

from apps.account.models import User

from PIL import Image
import os
from pathlib import Path


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


class PersonalAreaSerializer(serializers.ModelSerializer):
    """
    Сериализатор личного кабинета
    """
    class Meta:
        model = User
        fields = ('post_agreement', 'email', 'avatar', 'first_name', 'last_name',)

        extra_kwargs = {
            'role': {'read_only': True},
            'email': {'read_only': True},
            'avatar': {'allow_null': True, 'use_url': False},
            # 'first_name': {'validators': [validate_letters]},
            # 'last_name': {'validators': [validate_letters]}
            'first_name': {'read_only': True},
            'last_name': {'read_only': True}
        }

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if validated_data.get("avatar") is not None:
            image = Image.open(instance.avatar.path)
            image = image.convert("RGB")
            width, height = image.size
            if width > 300 and height > 300:
                # keep ratio but shrink down
                image.thumbnail((width, height))

            # check which one is smaller
            if height < width:
                # make square by cutting off equal amounts left and right
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                image = image.crop((left, top, right, bottom))

            elif width < height:
                # make square by cutting off bottom
                left = 0
                right = width
                top = 0
                bottom = width
                image = image.crop((left, top, right, bottom))

            if width > 300 and height > 300:
                image.thumbnail((300, 300))
            width, height = image.size  # Get new dimensions
            image.save(instance.avatar.path, format="webp",
                       quality=70, optimize=True)
            os.rename(instance.avatar.path,
                      Path(instance.avatar.path).with_suffix(".webp"))
            instance.avatar.name = instance.avatar.name.split(".")[0] + ".webp"
            instance.save()

        return instance
