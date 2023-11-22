from django.views.generic import TemplateView
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import redirect, reverse
from apps.studio.models import ChannelVideos
from apps.studio.forms import PlaylistForm

from apps.channel.models import Playlist
from django.contrib.auth.mixins import LoginRequiredMixin
from turbo_response import TurboStreamResponse, TurboStream

from guardian.shortcuts import get_objects_for_user


class StudioContentView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/contents/index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'content'
        })


class LoadStudioVideosContentView(LoginRequiredMixin, TemplateView):
    template_name = "pages/studio/contents/videos/index.html"

    def get(self, request, *args, **kwargs):
        # videos = ChannelVideos.objects.filter(channel__uid=kwargs['channel_uid'])
        videos = get_objects_for_user(request.user, perms=['studio.view_channelvideos'], klass=ChannelVideos, with_superuser=False)
        paginator = Paginator(videos, 4)
        page = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        return self.render_to_response({
            'page_obj': page_obj,
            'videos': videos,
            'end': ((page_obj.number - 1) * 4) + page_obj.object_list.count(),
            'start': (page_obj.number - 1) * 4 + 1
        })


class LoadStudioPlaylistsContentView(LoginRequiredMixin, TemplateView):
    template_name = "pages/studio/contents/playlists/index.html"

    def get(self, request, *args, **kwargs):
        permissions = [
            'channel.add_playlist',
            'channel.change_playlist',
            'channel.delete_playlist',
            'channel.view_playlist']

        playlists = get_objects_for_user(request.user, perms=permissions, klass=Playlist, with_superuser=False)
        paginator = Paginator(playlists, 4)
        page = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        return self.render_to_response({
            'page_obj': page_obj,
            'playlists': playlists,
            'end': ((page_obj.number - 1) * 4) + page_obj.object_list.count(),
            'start': (page_obj.number - 1) * 4 + 1
        })


class StudioPlaylistCreationView(LoginRequiredMixin, TemplateView):
    template_name = "pages/studio/contents/playlists/form.html"

    def get(self, request, *args, **kwargs):
        form = PlaylistForm()
        return self.render_to_response({
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PlaylistForm(request.POST)
        permissions = [
            'channel.add_playlist',
            'channel.change_playlist',
            'channel.delete_playlist',
            'channel.view_playlist']
        my_playlists = get_objects_for_user(request.user, perms=permissions, klass=Playlist, with_superuser=False)

        if form.is_valid():
            channel = request.user.channel

            if not my_playlists.filter(name=form.cleaned_data['name']).exists():
                Playlist.objects.create(channel=channel, **form.cleaned_data)
                redirect_to = reverse('studio:content', args=[channel.uid]) + '?section=playlists'
                return redirect(redirect_to)

        return TurboStreamResponse([
            TurboStream(request.turbo.frame).update.template("pages/studio/contents/playlists/form.html",
                                                             {'form': form}).response(request).rendered_content
        ])


class LoadStudioPodcastsContentView(LoginRequiredMixin, TemplateView):
    template_name = "pages/studio/contents/podcasts/index.html"


class LoadStudioLiveContentView(LoginRequiredMixin, TemplateView):
    template_name = "pages/studio/contents/live/index.html"


class LoadStudioPromotionsContentView(LoginRequiredMixin, TemplateView):
    template_name = "pages/studio/contents/promotions/index.html"
