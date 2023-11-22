from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from apps.accounts.models import User
from apps.channel.models import Channel, Topic, Playlist


# Create your models here.
class ChannelVideos(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE, limit_choices_to={'model__in': ('video', 'videodraft')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return str(self.item)


class VideoDraft(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    source = models.FileField(upload_to='videos')
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    topics = models.ManyToManyField(Topic, related_name='drafts', blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='drafts', null=True, blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, default='video/mp4')

    width = models.PositiveIntegerField(default=1280, blank=True)
    height = models.PositiveIntegerField(default=720, blank=True)
    fps = models.PositiveIntegerField(default=25, blank=True)

    thumbnails = GenericRelation('VideoThumbnail')

    def get_model_name(self):
        return self._meta.model_name

    def __str__(self):
        return self.title


class VideoThumbnail(models.Model):
    class Status(models.TextChoices):
        DEFAULT = "DEFAULT", "Default Thumbnail"
        NONE = "NONE", "Not Default"
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='thumbnails')
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    source = models.ImageField(upload_to='videos/thumbnails/', blank=True)
    alt = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NONE)

