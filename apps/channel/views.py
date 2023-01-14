from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.channel.models import ChannelsModel, UsersChannelModel
from apps.channel.serializers import ListChannelSerializers, DetailChannelSerializers
from apps.channel.permission import IsAuthenticatedOrReadOnly

from django.db.models import Q


class ListChannelView(ListCreateAPIView):
    serializer_class = ListChannelSerializers
    queryset = ChannelsModel.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if bool(self.request.user and self.request.user.is_authenticated):
            return queryset.filter(Q(userschannelmodel__user=self.request.user) | Q(is_private=False)).order_by('pk')
        else:
            return queryset.filter(is_private=False)


class DetailChannelView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailChannelSerializers
    queryset = ChannelsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if bool(self.request.user and self.request.user.is_authenticated):
            return queryset.filter(Q(userschannelmodel__user=self.request.user) | Q(is_private=False)).order_by('pk')
        else:
            return queryset.filter(is_private=False)

