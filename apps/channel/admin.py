from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.contrib.contenttypes.admin import GenericStackedInline

from apps.channel.models import Channel, ChannelPicture, Playlist, Video, Topic, ChannelBanner, ChannelLayout, \
    ChannelLayoutSection, ChannelVideoSection, Reply, Comment, Contact, ChannelLink


# Register your models here.
@admin.register(Channel)
class ChannelAdmin(GuardedModelAdmin):
    exclude = ['slug']


@admin.register(Contact)
class ContactAdmin(GuardedModelAdmin):
    pass


@admin.register(ChannelLink)
class ChannelLinkAdmin(GuardedModelAdmin):
    pass


class ChannelLayoutSectionInline(admin.StackedInline):
    model = ChannelLayoutSection


class ChannelVideoSectionInline(GenericStackedInline):
    model = ChannelLayoutSection


@admin.register(ChannelLayout)
class ChannelLayoutAdmin(GuardedModelAdmin):
    inlines = [ChannelLayoutSectionInline]


@admin.register(Reply)
class ReplyAdmin(GuardedModelAdmin):
    list_display = ['id', 'reference', 'reply_to', 'created']
    readonly_fields = ['user']
    list_filter = ['user']


@admin.register(Comment)
class CommentAdmin(GuardedModelAdmin):
    list_display = ['id', 'content', 'user', 'created']
    readonly_fields = ['user']
    list_filter = ['user']


@admin.register(ChannelLayoutSection)
class ChannelLayoutSectionAdmin(GuardedModelAdmin):
    # inlines = [ChannelVideoSectionInline]
    pass


@admin.register(ChannelVideoSection)
class ChannelVideoSectionAdmin(GuardedModelAdmin):
    inlines = [ChannelVideoSectionInline]


@admin.register(ChannelPicture)
class ChannelPictureAdmin(GuardedModelAdmin):
    pass


@admin.register(ChannelBanner)
class ChannelBannerAdmin(GuardedModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(GuardedModelAdmin):
    exclude = ['users_like', 'users_dislike']
    readonly_fields = ['uid']
    list_filter = ['author']


@admin.register(Playlist)
class PlaylistAdmin(GuardedModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(GuardedModelAdmin):
    exclude = ['slug']