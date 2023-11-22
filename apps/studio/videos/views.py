import http

from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import TemplateView
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.contrib.contenttypes.models import ContentType
from apps.channel.models import Video, Comment, Topic
from apps.studio.models import VideoThumbnail
from apps.studio.forms import VideoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from turbo_response import TurboStreamResponse, TurboStream


class StudioVideoDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/details/index.html'
    video = None
    thumbnails = None

    def dispatch(self, request, *args, **kwargs):
        self.video = get_object_or_404(Video, id=kwargs['video_id'])
        self.thumbnails = VideoThumbnail.objects.filter(object_id=self.video.id, content_type=ContentType.objects.get_for_model(self.video))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = VideoForm(user=request.user, instance=self.video)

        return self.render_to_response({
            'video': self.video,
            'topics': Topic.objects.all(),
            'form': form,
            'page': 'video-detail',
            'thumbnails': self.thumbnails
        })

    def post(self, request, *args, **kwargs):
        form = VideoForm(user=request.user, instance=self.video, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect(reverse("studio:video-detail", args=[kwargs['channel_uid'], kwargs['video_id']]))
        status = http.HTTPStatus.UNPROCESSABLE_ENTITY

        return self.render_to_response({
            'form': form,
            'video': self.video,
            'page': 'video-detail',
            'thumbnails': self.thumbnails
        }, status=status)


class StudioVideoTopicsSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/video/topics/form.html'

    def get(self, request, *args, **kwargs):
        video = get_object_or_404(Video, id=kwargs['video_id'])
        topics = Topic.objects.exclude(name__in=[item for item in video.topics.values_list('name', flat=True)])
        query = None
        results = None

        if 'search' in request.GET:
            query = request.GET.get('search')
            results = topics.filter(name__icontains=query)

        context = {
            'topics': results,
            'query': query,
            'video': video
        }

        if request.turbo.frame and request.turbo.has_turbo_header:
            return TurboStreamResponse([
                TurboStream("topics-list-with-pagination").update.template("pages/studio/details/topics/list.html", context).response(request).rendered_content
            ])
        return self.render_to_response(context)


class StudioVideoAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/details/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page': 'video-analytics',
            'video': get_object_or_404(Video, id=kwargs['video_id'])
        })
        return context


class StudioVideoEditorView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/details/editor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page': 'video-editor',
            'video': get_object_or_404(Video, id=kwargs['video_id'])
        })
        return context


class StudioVideoCommentsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/details/comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page': 'video-comments',
            'video': get_object_or_404(Video, id=kwargs['video_id'])
        })
        return context


class StudioVideoFetchCommentsView(LoginRequiredMixin, TemplateView):
    template_name = 'components/pages/studio/comments/_list.html'

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(video=kwargs['video_id'])
        page = request.GET.get('page')
        paginator = Paginator(comments, 4)

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        return self.render_to_response({
            'comments': comments,
            'page_obj': page_obj,
            'end': ((page_obj.number - 1) * 4) + page_obj.object_list.count(),
            'start': (page_obj.number - 1) * 4 + 1,
            'is_details': True
        })
