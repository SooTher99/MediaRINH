from django.urls import path
from apps.channel.views import ListChannelView, DetailChannelView

urlpatterns = [
    path('channels/', ListChannelView.as_view(), name='channels'),
    path('channels/<int:pk>/', DetailChannelView.as_view(), name='channel'),
]