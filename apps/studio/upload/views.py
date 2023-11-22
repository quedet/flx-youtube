import cv2

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.base import ContentFile
from turbo_response import TurboStreamResponse, TurboStream
from django.core.files import File
from django.contrib.auth.mixins import LoginRequiredMixin

from PIL import Image
from io import BytesIO

from moviepy.editor import VideoFileClip


from apps.studio.models import VideoDraft, VideoThumbnail, ChannelVideos
from apps.channel.models import Video, Topic
from apps.studio.forms import VideoDraftForm


class StudioUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/upload.html'
    channel = None

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'contents'
        })

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        type = request.POST.get('type')
        video = request.FILES.get('source')
        user = request.user
        mime_type = str(type).split('/')[0]
        sub_type = str(type).split('/')[1]

        if video and mime_type == 'video':
            new_draft = VideoDraft.objects.create(author=user, source=video, title=title, type=type)
            if new_draft:
                # if sub_type != 'mp4':
                #     from_path = new_draft.source.path
                #     to_path = str(from_path).replace(sub_type.lower(), 'mp4')
                #     clip = VideoFileClip(from_path)
                #     clip.write_videofile(to_path, fps=clip.fps)
                #
                #     new_draft.source.delete()
                #     new_draft.source.path = to_path
                #     new_draft.save()
                #
                #     clip.close()

                vid = cv2.VideoCapture(new_draft.source.path)
                new_draft.width = round(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                new_draft.height = round(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                new_draft.fps = round(vid.get(cv2.CAP_PROP_FPS))
                new_draft.save()

                ChannelVideos.objects.create(channel=user.channel, item=new_draft)
            return HttpResponse(f"{new_draft.id}")
        return HttpResponseBadRequest()


class StudioDraftUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/publishing.html'
    draft = None

    def dispatch(self, request, *args, **kwargs):
        self.draft = get_object_or_404(VideoDraft, id=kwargs['draft_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = VideoDraftForm(instance=self.draft)

        return self.render_to_response({
            'form': form,
            'draft': self.draft
        })

    def post(self, request, *args, **kwargs):
        form = VideoDraftForm(instance=self.draft, data=request.POST, files=request.FILES)
        thumbnail_selected = request.POST.get('thumbnails')

        if form.is_valid():
            if thumbnail_selected:
                thumbnail = VideoThumbnail.objects.get(id=thumbnail_selected, object_id=self.draft.id, content_type=ContentType.objects.get_for_model(self.draft))
                self.draft.thumbnail = thumbnail.source
                self.draft.save()

            form.save()

            return TurboStreamResponse([
                TurboStream("upload--renderer--message").update.template("pages/studio/publishing/success.html")
                .response(request=self.request).rendered_content
            ])
        else:
            return TurboStreamResponse([
                TurboStream("upload--renderer--message").update.template("pages/studio/publishing/error.html")
                .response(request=self.request).rendered_content
            ])


class StudioDraftTopicsSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/video/topics/form.html'

    def get(self, request, *args, **kwargs):
        video = get_object_or_404(VideoDraft, id=kwargs['draft_id'])
        topics = Topic.objects.exclude(name__in=[item for item in video.topics.values_list('name', flat=True)])
        query = None
        results = None

        print(video)

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


class GenerateVideosThumbnailsView(LoginRequiredMixin, TemplateView):
    template_name = 'components/blocks/studio/_thumbnails.html'
    draft = None

    def dispatch(self, request, *args, **kwargs):
        self.draft = get_object_or_404(VideoDraft, id=kwargs['draft_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'draft': self.draft
        })

    def post(self, request, *args, **kwargs):
        if self.draft.thumbnails.count() == 0:
            video = VideoFileClip(self.draft.source.path)
            duration = round(video.duration)

            middle_frame = round(duration / 2)
            frame_gap = round(middle_frame - (middle_frame / 2))
            second_frame = frame_gap
            third_frame = middle_frame + frame_gap

            frames = [2, second_frame, middle_frame, third_frame]

            for frame in frames:
                frame_data = video.get_frame(frame)
                img = Image.fromarray(frame_data, 'RGB')
                temp_thumb = BytesIO()

                img.save(temp_thumb, "JPEG")
                temp_thumb.seek(0)
                new_video = VideoThumbnail.objects.create(item=self.draft, alt=self.draft.title)
                new_video.source.save(f"{self.draft.title}.jpeg", ContentFile(temp_thumb.read()), save=True)
                temp_thumb.close()
        return self.render_to_response({
            'draft': self.draft
        })


class StudioPublishingView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        draft = get_object_or_404(VideoDraft, id=kwargs['draft_id'])
        if draft.title and draft.topics.count() > 0 and draft.source:
            channel_videos = ChannelVideos.objects.filter(channel=request.user.channel)

            try:
                video = Video.objects.get(title=draft.title)
            except Video.DoesNotExist:
                video = Video.objects.create(
                    title=draft.title,
                    description=draft.description,
                    author=draft.author,
                    source=draft.source,
                    thumbnail=draft.thumbnail,
                    type=draft.type,
                    width=draft.width,
                    height=draft.height,
                    fps=draft.fps
                )

                video.topics.set(draft.topics.all())
                video.save()

            video_type = ContentType.objects.get_for_model(video)

            if not channel_videos.filter(content_type=video_type, object_id=video.id).exists():
                ChannelVideos.objects.create(channel=request.user.channel, item=video)

            thumbnails = VideoThumbnail.objects.filter(content_type=ContentType.objects.get_for_model(draft))

            for thumbnail in thumbnails:
                thumbnail.content_type = video_type
                thumbnail.object_id = video.id
                thumbnail.save()

            channel_videos.filter(content_type=ContentType.objects.get_for_model(draft), object_id=draft.id).delete()
            draft.delete()

            return redirect(video.get_absolute_url())
        return HttpResponse("ok")
