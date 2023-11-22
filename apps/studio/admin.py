from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from apps.studio.models import ChannelVideos, VideoDraft, VideoThumbnail


# Register your models here.
@admin.register(ChannelVideos)
class ChannelVideosAdmin(GuardedModelAdmin):
    list_filter = ['channel']


@admin.register(VideoDraft)
class VideoDraftAdmin(GuardedModelAdmin):
    list_filter = ['author']


@admin.register(VideoThumbnail)
class VideoThumbnailAdmin(GuardedModelAdmin):
    pass
