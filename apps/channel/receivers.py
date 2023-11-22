from django.db.models.signals import post_save, m2m_changed
from guardian.shortcuts import assign_perm
from django.dispatch import receiver

from apps.channel.models import Channel, ChannelPicture, ChannelBanner, ChannelLayout, ChannelShortSection, \
    ChannelVideoSection, Comment, Reply, Video, Playlist, ChannelLink


@receiver(post_save, sender=Channel)
def channel_post_create(sender, instance, created, **kwargs):
    if created and instance.author is not None:
        permissions = [
            'channel.add_channel',
            'channel.change_channel',
            'channel.delete_channel',
            'channel.view_channel']

        for perm in permissions:
            assign_perm(perm, instance.author, instance)

        ChannelPicture.objects.create(channel=instance)
        ChannelBanner.objects.create(channel=instance)
        ChannelLayout.objects.create(channel=instance)


@receiver(post_save, sender=Playlist)
def playlist_post_create(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = [
            'channel.add_playlist',
            'channel.change_playlist',
            'channel.delete_playlist',
            'channel.view_playlist']

        for perm in permissions:
            assign_perm(perm, instance.channel.author, instance)


@receiver(post_save, sender=ChannelLink)
def channel_link_post_create(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = [
            'channel.add_channellink',
            'channel.change_channellink',
            'channel.delete_channellink',
            'channel.view_channellink']

        for perm in permissions:
            assign_perm(perm, instance.channel.author, instance)


@receiver(post_save, sender=ChannelLayout)
def channel_layout_post_create(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = [
            'channel.add_channellayout',
            'channel.change_channellayout',
            'channel.delete_channellayout',
            'channel.view_channellayout']

        for perm in permissions:
            assign_perm(perm, instance.channel.author, instance)


@receiver(post_save, sender=ChannelPicture)
def channel_picture_post_create(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = [
            'channel.add_channelpicture',
            'channel.change_channelpicture',
            'channel.delete_channelpicture',
            'channel.view_channelpicture']

        for perm in permissions:
            assign_perm(perm, instance.channel.author, instance)


@receiver(post_save, sender=ChannelBanner)
def channel_banner_post_create(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = [
            'channel.add_channelbanner',
            'channel.change_channelbanner',
            'channel.delete_channelbanner',
            'channel.view_channelbanner']

        for perm in permissions:
            assign_perm(perm, instance.channel.author, instance)


@receiver(post_save, sender=ChannelVideoSection)
def channel_video_section_post_create(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = [
            'channel.add_channelshortsection',
            'channel.change_channelshortsection',
            'channel.delete_channelshortsection',
            'channel.view_channelshortsection']

        for perm in permissions:
            assign_perm(perm, instance.user, instance)


@receiver(post_save, sender=ChannelShortSection)
def channel_short_section_post_create(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = [
            'channel.add_ChannelShortSection',
            'channel.change_ChannelShortSection',
            'channel.delete_ChannelShortSection',
            'channel.view_ChannelShortSection']

        for perm in permissions:
            assign_perm(perm, instance.user, instance)


@receiver(post_save, sender=Comment)
def comment_post_create(sender, instance, created, **kwargs):
    if created and instance.user is not None:
        permissions = [
            'channel.add_comment',
            'channel.change_comment',
            'channel.delete_comment',
            'channel.view_comment']

        for perm in permissions:
            assign_perm(perm, instance.user, instance)


@receiver(post_save, sender=Reply)
def reply_post_create(sender, instance, created, **kwargs):
    if created and instance.user is not None:
        permissions = [
            'channel.add_reply',
            'channel.change_reply',
            'channel.delete_reply',
            'channel.view_reply']

        for perm in permissions:
            assign_perm(perm, instance.user, instance)


@receiver(m2m_changed, sender=Comment.users_like.through)
def comment_users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()


@receiver(m2m_changed, sender=Reply.users_like.through)
def reply_users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()


@receiver(m2m_changed, sender=Video.users_like.through)
def video_users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
