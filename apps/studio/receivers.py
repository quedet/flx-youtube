from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from guardian.shortcuts import assign_perm
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


from moviepy.editor import VideoFileClip
from time import strftime, gmtime

from apps.studio.models import VideoDraft, VideoThumbnail, ChannelVideos
from apps.channel.models import Video


@receiver(post_save, sender=ChannelVideos)
def channel_videos_post_save(sender, instance, created, **kwargs):
    if created and instance.channel is not None:
        permissions = ['studio.view_channelvideos', 'studio.change_channelvideos', 'studio.delete_channelvideos',
                       'studio.add_channelvideos']
        for perm in permissions:
            assign_perm(perm, instance.channel.author, instance)


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created and instance.author is not None:
        permissions = ['channel.view_video', 'channel.change_video', 'channel.delete_video', 'channel.add_video']
        for perm in permissions:
            assign_perm(perm, instance.author, instance)

    if instance.source:
        video = VideoFileClip(instance.source.path)

        if not instance.thumbnail:
            frame_data = video.get_frame(2)
            img = Image.fromarray(frame_data, 'RGB')
            temp_thumb = BytesIO()

            img.save(temp_thumb, "JPEG")
            temp_thumb.seek(0)
            instance.thumbnail.save(f"{instance.title}.jpeg", ContentFile(temp_thumb.read()), save=True)
            temp_thumb.close()

        if not instance.duration:
            duration = gmtime(video.duration)

            if duration.tm_hour > 0:
                instance.duration = strftime("%H:%M:%S", duration)
            else:
                instance.duration = strftime("%M:%S", duration)
            instance.save()


@receiver(post_save, sender=VideoDraft)
def video_draft_post_save(sender, instance, created, **kwargs):
    if created and instance.author is not None:
        permissions = ['studio.view_videodraft', 'studio.change_videodraft', 'studio.delete_videodraft',
                       'studio.add_videodraft']
        for perm in permissions:
            assign_perm(perm, instance.author, instance)

    if instance.source:
        video = VideoFileClip(instance.source.path)
        duration = round(video.duration)

        middle_frame = round(duration / 2)
        frame_gap = round(middle_frame - (middle_frame / 2))
        second_frame = frame_gap
        third_frame = middle_frame + frame_gap

        frames = [2, second_frame, middle_frame, third_frame]

        if not instance.thumbnail:
            frame_data = video.get_frame(2)
            img = Image.fromarray(frame_data, 'RGB')
            temp_thumb = BytesIO()

            img.save(temp_thumb, "JPEG")
            temp_thumb.seek(0)
            instance.thumbnail.save(f"{instance.title}.jpeg", ContentFile(temp_thumb.read()), save=True)
            temp_thumb.close()

        if not instance.thumbnails:
            for frame in frames:
                frame_data = video.get_frame(frame)
                img = Image.fromarray(frame_data, 'RGB')
                temp_thumb = BytesIO()

                img.save(temp_thumb, "JPEG")
                temp_thumb.seek(0)
                new_video = VideoThumbnail.objects.create(video=instance, alt=instance.title)
                new_video.source.save(f"{instance.title}.jpeg", ContentFile(temp_thumb.read()), save=True)
                temp_thumb.close()

        if not instance.duration:
            duration = gmtime(video.duration)

            if duration.tm_hour > 0:
                instance.duration = strftime("%H:%M:%S", duration)
            else:
                instance.duration = strftime("%M:%S", duration)
            instance.save()


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.source:
        instance.source.delete(save=False)

    if instance.thumbnail:
        instance.thumbnail.delete(save=False)
