import redis, cv2

from django.shortcuts import redirect, get_object_or_404, reverse
from django.views.generic import TemplateView

from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector, TrigramSimilarity, TrigramWordSimilarity

# Create your views here.
from apps.channel.models import Video, Topic, Reply, Comment

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class HomePageView(TemplateView):
    template_name = "pages/assets/index.html"

    def get(self, request, *args, **kwargs):
        topics = Topic.objects.annotate(video_counts=Count('videos')).filter(video_counts__gt=0).values('name', 'slug')

        return self.render_to_response({
            'topics': topics,
            # 'placeholder_range': range(10)
        })


class VideoFetcherView(TemplateView):
    template_name = "components/blocks/videos/_lists.html"

    def get(self, request, *args, **kwargs):
        topic_slug = request.GET.get('topic')
        videos = Video.objects.all()

        if topic_slug and topic_slug != 'all':
            videos = videos.filter(topics__slug__in=[topic_slug])

        paginator = Paginator(videos, 10)
        page = request.GET.get('page')

        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            return HttpResponse('')
            # videos = paginator.page(paginator.num_pages)

        return self.render_to_response({
            'videos': videos
        })


class VideoPreviewView(TemplateView):
    template_name = 'components/blocks/videos/_preview.html'

    def get(self, request, *args, **kwargs):
        video = get_object_or_404(Video, uid=kwargs['uid'])

        self.render_to_response({
            'video': video
        })


class FetchRelatedVideoView(TemplateView):
    template_name = "components/blocks/videos/_related_lists.html"

    def get(self, request, *args, **kwargs):
        topic_slug = request.GET.get('topic')
        related_videos = Video.objects.exclude(uid=kwargs['uid'])

        if topic_slug and topic_slug != 'all':
            videos = related_videos.filter(topics__slug__in=[topic_slug])

            if videos.count() == 0:
                videos = related_videos.filter(author__channel__pseudo=topic_slug)

            related_videos = videos

        paginator = Paginator(related_videos, 20)
        page = request.GET.get('page')

        try:
            related_videos = paginator.page(page)
        except PageNotAnInteger:
            related_videos = paginator.page(1)
        except EmptyPage:
            related_videos = paginator.page(paginator.num_pages)
            return HttpResponse('')

        return self.render_to_response({
            'related_videos': related_videos
        })


class DetailView(TemplateView):
    template_name = "pages/assets/detail.html"
    video = None

    def dispatch(self, request, *args, **kwargs):
        video_uid = request.GET.get('v')

        if not video_uid:
            return redirect('assets:index')

        self.video = get_object_or_404(Video, uid=video_uid)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # increment total video views by 1
        total_views = r.incr(f'video:{self.video.id}:views')
        # increment video ranking by 1
        r.zincrby(f'video_ranking', 1, self.video.id)
        # get video total comments including replies
        total_comments_count = sum([item.get_replies_count() for item in self.video.comments.all()]) + self.video.comments.count()

        return self.render_to_response({
            'video': self.video,
            'page': 'watching',
            'total_views': total_views,
            'total_comments_count': total_comments_count
        })


class FetchVideoCommentReplyView(TemplateView):
    template_name = 'components/blocks/comments/lists/_replies_list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs['comment_id'])
        replies = Reply.objects.filter(reference=comment)
        page = request.GET.get('page')
        paginator = Paginator(replies, 2)

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        next_page = None
        if page_obj.has_next():
            next_page = page_obj.next_page_number()

        return self.render_to_response({
            'next_page': next_page,
            'replies': page_obj.object_list,
            'user': request.user
        })


class FetchVideoCommentView(TemplateView):
    template_name = 'components/blocks/comments/lists/_comments_list.html'

    def get(self, request, *args, **kwargs):
        video = get_object_or_404(Video, uid=kwargs['uid'])
        comment = Comment.objects.filter(video=video)
        page = request.GET.get('page')
        paginator = Paginator(comment, 4)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            return HttpResponse('')

        return self.render_to_response({
            'comments': page_obj.object_list,
            'user': request.user
        })


class VideoSearchIndexView(TemplateView):
    template_name = 'pages/search/index.html'

    def get(self, request, *args, **kwargs):
        results = None

        if 'query' in request.GET:
            query = request.GET.get('query')
            if str(query).strip() != '':
                title_similarity = TrigramWordSimilarity(query, 'title')
                description_similarity = TrigramWordSimilarity(query, 'description')
                channel_similarity = TrigramWordSimilarity(query, 'author__channel__name')

                results = Video.objects.annotate(similarity=title_similarity + description_similarity + channel_similarity)\
                    .filter(similarity__gt=0.3)\
                    .order_by('-similarity')

        return self.render_to_response({
            'results': results,
            'page': 'search'
        })


class VideoSearchResultsView(TemplateView):
    template_name = 'pages/search/results.html'

    def get(self, request, *args, **kwargs):
        results = None

        if 'query' in request.GET:
            query = request.GET.get('query')

            if str(query).strip() != '':
                title_similarity = TrigramWordSimilarity(query, 'title')
                description_similarity = TrigramWordSimilarity(query, 'description')
                channel_similarity = TrigramWordSimilarity(query, 'author__channel__name')
                results = Video.objects.annotate(similarity=title_similarity + description_similarity + channel_similarity)\
                    .filter(similarity__gt=0.3)\
                    .order_by('-similarity')

        return self.render_to_response({
            'results': results
        })

