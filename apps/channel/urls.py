from django.urls import path
from apps.channel.views import ChannelView

urlpatterns = [
    path('channels/', ChannelView.as_view(), name='channels'),
]