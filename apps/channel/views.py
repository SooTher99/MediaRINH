from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status

from apps.channel.models import ChannelsModel, UsersChannelModel
from apps.channel.serializers import (ListChannelSerializers,
                                      DetailChannelSerializers,
                                      ListUserSerializers,
                                      AddUserInChannelSerializers,
                                      UserInChannelSerializers)
from apps.channel.permission import IsAuthenticatedOrReadOnly
from apps.account.models import User

from django.db.models import Q
from django.shortcuts import get_object_or_404


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


class AddUsersInChannelView(GenericAPIView):
    serializer_class = AddUserInChannelSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['username']

    def get_context(self):
        return get_object_or_404(ChannelsModel.objects.filter(pk=self.kwargs.get('pk')))

    def get_queryset(self):
        queryset = super().get_queryset()
        user_channel = UsersChannelModel.objects.filter(channel=self.kwargs.get('pk')).values_list('user__id',
                                                                                                   flat=True)
        return queryset.filter(is_staff=False, is_active=True).exclude(pk__in=user_channel)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListUserSerializers
        else:
            return AddUserInChannelSerializers

    def post(self, request, *args, **kwargs):
        channel = self.get_context()
        serializer = self.get_serializer(data=request.data, context={'users_instance': self.get_queryset()})
        serializer.is_valid(raise_exception=True)
        serializer.save(channel=channel)

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListUserInChannel(ListAPIView):
    serializer_class = UserInChannelSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UsersChannelModel.objects.all()

    def get_queryset(self):
        quer = super().get_queryset().filter(channel=self.kwargs.get('pk'))
        return quer




