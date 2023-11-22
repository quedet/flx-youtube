import random, string, redis

from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from youtube.utils import generate_uid
from apps.accounts.models import User
from apps.channel.fields import OrderField

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


# Create your models here.
def generate_pseudo(name):
    pseudo = ''.join(str(name).split(' '))

    if not Channel.objects.filter(pseudo=pseudo).exists():
        return pseudo
    else:
        return pseudo + ''.join(random.sample(string.digits, 4))


def get_channel_original_picture_url(self, filename):
    extension = filename.split('.')[-1]
    return f"channels/{self.channel.uid}/picture/temp/channel_picture.{str(extension).lower()}"


def get_channel_cropped_picture_url(self, filename):
    extension = filename.split('.')[-1]
    return f"channels/{self.channel.uid}/picture/channel_thumbnail.{str(extension).lower()}"


def get_channel_original_banner_url(self, filename):
    extension = filename.split('.')[-1]
    return f"channels/{self.channel.uid}/banner/temp/channel_banner.{str(extension).lower()}"


def get_channel_cropped_banner_url(self, filename):
    extension = filename.split('.')[-1]
    return f"channels/{self.channel.uid}/banner/channel_banner.{str(extension).lower()}"


class Channel(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(5)])
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='channel')
    description = models.TextField(null=True, blank=True)
    pseudo = models.CharField(max_length=100, unique=True, null=True, blank=True)
    uid = models.CharField(max_length=24, unique=True, null=True, blank=True)
    followers = models.ManyToManyField(User, through='Contact', related_name='followings', symmetrical=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.uid:
            self.uid = generate_uid()

        if not self.pseudo:
            self.pseudo = generate_pseudo(self.name)

        if update_fields is not None and "name" in update_fields:
            self.pseudo = generate_pseudo(self.name)

        return super().save(force_insert, force_update, using, update_fields)

    # Statistics
    def get_total_views(self):
        views = sum([item.get_total_views() for item in self.author.video_set.all()])
        return views

    def get_total_likes(self):
        likes = sum([item.get_total_likes() for item in self.author.video_set.all()])
        return likes

    def get_total_dislikes(self):
        dislikes = sum([item.get_total_dislikes() for item in self.author.video_set.all()])
        return dislikes

    def get_total_comments(self):
        total_comments = self.author.comments.count()
        total_replies = sum([item.get_replies_count() for item in self.author.comments.all()])
        return total_replies + total_comments

    def get_total_subscribers(self):
        return self.followers.count()

    # Links
    def get_absolute_url(self):
        return reverse("channel:home", args=[self.pseudo])

    def get_dashboard_url(self):
        return reverse("studio:dashboard", args=[self.uid])

    def get_contents_url(self):
        return reverse("studio:content", args=[self.uid])

    def get_analytics_url(self):
        return reverse("studio:analytics", args=[self.uid])

    def get_comments_url(self):
        return reverse("studio:comments", args=[self.uid])

    def get_subtitles_url(self):
        return reverse("studio:subtitles", args=[self.uid])

    def get_earn_url(self):
        return reverse("studio:earn", args=[self.uid])

    def get_copyright_url(self):
        return reverse("studio:copyright", args=[self.uid])

    def get_customization_url(self):
        return reverse("studio:customization", args=[self.uid])

    def get_audio_url(self):
        return reverse("studio:audio-library", args=[self.uid])


class ChannelPicture(models.Model):
    channel = models.OneToOneField(Channel, on_delete=models.CASCADE, related_name='picture')
    original = models.ImageField(upload_to=get_channel_original_picture_url, blank=True,
                                 default='no-image-available.png')
    cropped = models.ImageField(upload_to=get_channel_cropped_picture_url, blank=True)
    cropX = models.IntegerField(blank=True, null=True)
    cropY = models.IntegerField(blank=True, null=True)
    cropWidth = models.IntegerField(blank=True, null=True)
    cropHeight = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, default='image/png')


class ChannelBanner(models.Model):
    channel = models.OneToOneField(Channel, on_delete=models.CASCADE, related_name='banner')
    original = models.ImageField(upload_to=get_channel_original_banner_url, blank=True,
                                 default='no-image-available.png')
    cropped = models.ImageField(upload_to=get_channel_cropped_banner_url, blank=True)
    cropX = models.IntegerField(blank=True, null=True)
    cropY = models.IntegerField(blank=True, null=True)
    cropWidth = models.IntegerField(blank=True, null=True)
    cropHeight = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, default='image/png')


class ChannelLink(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=200)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = OrderField(for_fields=['channel'])

    class Meta:
        ordering = ['order']


class Playlist(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['slug']),
            models.Index(fields=['name'])
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        name_slugged = slugify(self.name)
        self.slug = f"{self.channel.uid}-{name_slugged}"

        if update_fields is not None and "name" in update_fields:
            update_fields = {"slug"}.union(update_fields)

        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name

    # Statistics
    def get_total_views(self):
        return sum([item.get_total_views() for item in self.videos.all()])

        # Statistics

    def get_total_likes(self):
        likes = sum([item.get_total_likes() for item in self.videos.all()])
        return likes

    def get_total_dislikes(self):
        dislikes = sum([item.get_total_dislikes() for item in self.videos.all()])
        return dislikes

    def get_total_comments(self):
        return sum([item.get_total_comments() for item in self.videos.all()])


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    # total_videos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.name)

        if update_fields is not None and "name" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        return super().save(force_insert, force_update, using, update_fields)


class Video(models.Model):
    title = models.CharField(max_length=255)
    uid = models.CharField(max_length=12, unique=True, null=True)
    description = models.TextField(null=True, blank=True)
    source = models.FileField(upload_to='videos')
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name='videos', blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=25, default='video/mp4')
    width = models.PositiveIntegerField(default=1280, blank=True)
    height = models.PositiveIntegerField(default=720, blank=True)
    fps = models.PositiveIntegerField(default=25, blank=True)

    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)

    users_like = models.ManyToManyField(User, related_name='videos_liked', blank=True)
    users_dislike = models.ManyToManyField(User, related_name='videos_disliked', blank=True)

    total_likes = models.PositiveBigIntegerField(default=0)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        import random
        import string

        phrase = string.ascii_letters + string.digits + '-_'
        sample = random.sample(phrase, 12)

        if not self.uid:
            self.uid = ''.join(sample)

        return super().save(force_insert, force_update, using,update_fields)

    def __str__(self):
        return self.title

    # Statistics
    def get_total_views(self):
        return int(r.get(f'video:{self.id}:views'))

    def get_total_likes(self):
        return self.users_like.count()

    def get_total_dislikes(self):
        return self.users_dislike.count()

    def get_model_name(self):
        return self._meta.model_name

    def get_total_comments(self):
        return self.comments.count() + sum([item.get_replies_count() for item in self.comments.all()])

    # Links
    def get_absolute_url(self):
        return reverse('assets:detail') + f"?v={self.uid}"

    def get_edition_url(self):
        return reverse('studio:video-detail', args=[self.author.channel.uid, self.id])

    def get_analytics_url(self):
        return reverse('studio:video-analytics', args=[self.author.channel.uid, self.id])

    def get_editor_url(self):
        return reverse('studio:video-editor', args=[self.author.channel.uid, self.id])

    def get_comments_url(self):
        return reverse('studio:video-comments', args=[self.author.channel.uid, self.id])

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes'])
        ]


class Short(models.Model):
    title = models.CharField(max_length=255)
    uid = models.CharField(max_length=12, unique=True, null=True)
    caption = models.TextField(null=True, blank=True)
    source = models.FileField(upload_to='shorts')
    thumbnail = models.ImageField(upload_to='shorts/thumbnails/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name='shorts')
    duration = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    users_like = models.ManyToManyField(User, related_name='short_liked', blank=True)
    users_dislike = models.ManyToManyField(User, related_name='short_disliked', blank=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        import random
        import string

        phrase = string.ascii_letters + string.digits + '-_'
        sample = random.sample(phrase, 12)

        if not self.uid:
            self.uid = ''.join(sample)

        return super().save(force_insert, force_update, using,update_fields)

    def __str__(self):
        return self.title

    def get_total_views(self):
        return int(r.get(f'video:{self.id}:views'))

    def get_model_name(self):
        return self._meta.model_name

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]


class ChannelLayout(models.Model):
    channel = models.OneToOneField(Channel, on_delete=models.CASCADE, related_name='layout')
    trailer = models.OneToOneField(Video, on_delete=models.CASCADE, null=True, blank=True)


class ChannelLayoutSection(models.Model):
    layout = models.ForeignKey(ChannelLayout, on_delete=models.CASCADE, related_name='featured_sections')
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('channelvideosection', 'channelshortsection')})

    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['layout'])

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['order'])
        ]


class ChannelVideoSection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)


class ChannelShortSection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    short = models.ForeignKey(Short, on_delete=models.CASCADE)




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', editable=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    replies = GenericRelation('Reply')
    users_like = models.ManyToManyField(User, related_name='comments_liked')
    users_dislike = models.ManyToManyField(User, related_name='comments_disliked')

    total_likes = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['-total_likes'])
        ]

    def get_model_name(self):
        return self._meta.model_name

    def get_replies_count(self):
        return self.replies.count()


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies', editable=False)
    reference = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')

    content = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    reply_to = GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    users_like = models.ManyToManyField(User, related_name='replies_liked')
    users_dislike = models.ManyToManyField(User, related_name='replies_disliked')

    total_likes = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['-total_likes'])
        ]

    def get_model_name(self):
        return self._meta.model_name


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(Channel, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
