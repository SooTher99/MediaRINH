from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.channel import models
from apps.account.models import User
from utils.validators import validate_letters
from utils.img_to_webp import img_to_webp


class ListChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.ChannelsModel
        fields = ('id', 'name', 'link_name', 'img', 'description', 'is_private')
        extra_kwargs = {
            'link_name': {"validators": [UniqueValidator(queryset=models.ChannelsModel.objects.all(),
                                                         message="Канал с таким названием уже существует"),
                                         validate_letters]},
        }

    def create(self, validated_data):
        instance = super().create(validated_data=validated_data)
        models.UsersChannelModel.objects.create(user=self.context.get('request').user,
                                                channel=instance,
                                                role=models.RoleUserChannel.ADMIN)
        return img_to_webp(instance)


class DetailChannelSerializers(ListChannelSerializers):
    class Meta:
        model = models.ChannelsModel
        fields = ('id', 'name', 'img', 'description')

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return img_to_webp(instance)


class ListUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'first_name', 'last_name', 'username')


class AddUserInChannelSerializers(serializers.Serializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    def validate(self, attrs):
        if attrs.get('users') not in self.context.get('users_instance'):
            raise serializers.ValidationError(
                {'user': 'Пользователя которого вы выбрали скорее всего уже вступлен в канал'})
        return attrs

    def create(self, validated_data):
        my_list = []
        for user in validated_data.get('users'):
            my_list.append(models.UsersChannelModel(channel=validated_data.get('channel'), user=user))
        instance = models.UsersChannelModel.objects.bulk_create(my_list)

        return instance


class UserInChannelSerializers(serializers.ModelSerializer):
    user = ListUserSerializers()

    class Meta:
        model = models.UsersChannelModel
        fields = ('id', 'user', 'role')
