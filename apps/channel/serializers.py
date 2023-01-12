from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.channel import models
from utils.validators import validate_letters


class ChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.ChannelsModel
        fields = ('id', 'name', 'link_name')
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
        return instance
