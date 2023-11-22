import redis

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.conf import settings

from apps.channel.models import Channel, Video, ChannelLayout

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


# Create your views here.
class FetchChannelVideosView(TemplateView):
    template_name = "components/blocks/videos/_lists.html"

    def get(self, request, *args, **kwargs):
        videos = Video.objects.filter(author__channel__pseudo=kwargs['channel_slug'])

        paginator = Paginator(videos, 8)
        page = request.GET.get('page')

        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            return HttpResponse('')

        return self.render_to_response({
            'videos': videos,
            'on_channel': True
        })


class ChannelHomeView(TemplateView):
    template_name = 'pages/channels/index.html'

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, pseudo=kwargs['channel_pseudo'])
        queryset = Video.objects.filter(author__channel=channel)
        video_ranking = r.zrange('video_ranking', 0, -1, desc=True)

        video_ranking_ids = [int(id) for id in video_ranking]

        most_viewed = list(queryset.filter(id__in=video_ranking_ids))
        most_viewed.sort(key=lambda x: video_ranking_ids.index(x.id))

        return self.render_to_response({
            'page_section': 'home',
            'channel': channel,
            'recent_videos': queryset.order_by('-created'),
            'popular_videos': most_viewed,
            'on_channel': True
        })


class ChannelAboutView(TemplateView):
    template_name = 'pages/channels/about.html'

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, pseudo=kwargs['channel_code__name'])
        return self.render_to_response({
            'page_section': 'about',
            'channel': channel
        })


class ChannelPlaylistsView(TemplateView):
    template_name = 'pages/channels/about.html'

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, pseudo=kwargs['channel_code__name'])
        return self.render_to_response({
            'page_section': 'playlists',
            'channel': channel
        })


class ChannelVideosView(TemplateView):
    template_name = 'pages/channels/videos.html'

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, pseudo=kwargs['channel_code__name'])
        return self.render_to_response({
            'page_section': 'videos',
            'channel': channel
        })


class ChannelCommunityView(TemplateView):
    template_name = 'pages/channels/community.html'

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, pseudo=kwargs['channel_code__name'])
        return self.render_to_response({
            'page_section': 'community',
            'channel': channel
        })