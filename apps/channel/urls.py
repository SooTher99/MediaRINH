from django.urls import path
from apps.channel.views import ListChannelView, DetailChannelView, AddUsersInChannelView, ListUserInChannel

urlpatterns = [
    path('channels/', ListChannelView.as_view(), name='channels'),
    path('channels/<int:pk>/', DetailChannelView.as_view(), name='channel'),
    path('channels/<int:pk>/add-users/', AddUsersInChannelView.as_view(), name='add-users'),
    path('channels/<int:pk>/users/', ListUserInChannel.as_view(), name='users')
]