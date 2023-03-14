from django.contrib import admin
from .models import MediaModel, ChannelsModel, UsersChannelModel

admin.site.register(MediaModel)
admin.site.register(ChannelsModel)
admin.site.register(UsersChannelModel)
