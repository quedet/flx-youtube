from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.channel.models import Video, Comment


# Create your views here.
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


class StudioCommentsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/comments/index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'comments',
        })


class LoadCommentsView(LoginRequiredMixin, TemplateView):
    template_name = 'components/pages/studio/comments/_list.html'

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(video__author=request.user)
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
            'start': (page_obj.number - 1) * 4 + 1
        })
