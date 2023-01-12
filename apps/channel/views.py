from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.channel.models import ChannelsModel
from apps.channel.serializers import ChannelSerializers


class ChannelView(ListCreateAPIView):
    serializer_class = ChannelSerializers
    queryset = ChannelsModel.objects.all()
    permission_classes = [IsAuthenticated]
