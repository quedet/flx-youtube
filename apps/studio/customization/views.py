import os, cv2

from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.files.base import File
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from turbo_response import TurboStreamResponse, TurboStream

from apps.channel.models import Channel, ChannelPicture, ChannelBanner, Video, ChannelLayout, ChannelLink
from apps.studio.customization.forms import ChannelBasicInfoForm, ChannelPictureForm, ChannelBannerForm

from braces.views import CsrfExemptMixin, JSONRequestResponseMixin


class StudioCustomizationBrandingPictureView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/customization/branding/picture.html'
    channel = None
    picture = None

    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel, uid=kwargs['channel_uid'])
        self.picture = get_object_or_404(ChannelPicture, channel=self.channel)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'form': ChannelPictureForm(instance=self.picture),
            'picture': self.picture
        })

    def post(self, request, *args, **kwargs):
        form = ChannelPictureForm(instance=self.picture, data=request.POST, files=request.FILES)
        uploaded_picture = request.FILES.get('original')
        cropX = int(float(request.POST.get('cropX')))
        cropY = int(float(request.POST.get('cropY')))
        cropWidth = int(float(request.POST.get('cropWidth')))
        cropHeight = int(float(request.POST.get('cropHeight')))

        if not os.path.exists(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}"):
            os.mkdir(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}")
        if not os.path.exists(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture"):
            os.mkdir(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture")
        if not os.path.exists(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture/temp"):
            os.mkdir(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture/temp")

        if not uploaded_picture and self.picture.original is None:
            return HttpResponseBadRequest()

        if self.picture.cropX != cropX:
            self.picture.cropX = cropX

        if self.picture.cropY != cropY:
            self.picture.cropY = cropY

        if self.picture.cropWidth != cropWidth:
            self.picture.cropWidth = cropWidth

        if self.picture.cropHeight != cropHeight:
            self.picture.cropHeight = cropHeight

        if self.picture.cropX != cropX or self.picture.cropY != cropY or self.picture.cropWidth != cropWidth or self.picture.cropHeight != cropHeight:
            self.picture.save()

        if uploaded_picture:
            picture_type = request.POST.get('type')
            picture_extension = picture_type.split('/')[-1]

            if self.picture.type != picture_type:
                self.picture.type = picture_type
                self.picture.save()

            self.picture.original.delete()
            self.picture.original.save(f"channel_picture.{picture_extension}", uploaded_picture)
        else:
            picture_extension = self.picture.type.split('/')[-1]

        original_url = f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture/temp/channel_picture.{picture_extension}"
        cropped_url = f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture/channel_thumbnail.{picture_extension}"

        image = cv2.imread(original_url)
        cropped_img = image[cropY:cropY + cropHeight, cropX:cropX + cropWidth]
        cv2.imwrite(cropped_url, cropped_img)

        self.picture.cropped.delete()
        self.picture.cropped.save(f"channel_thumbnail.{picture_extension}", File(open(cropped_url, 'rb')), save=False)
        self.picture.save()

        redirect_to = reverse('studio:customization', args=[self.channel.uid]) + '?section=branding'
        return HttpResponse(redirect_to)


class StudioCustomizationBrandingBannerView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/customization/branding/banner.html'
    channel = None
    banner = None

    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel, uid=kwargs['channel_uid'])
        self.banner = get_object_or_404(ChannelBanner, channel=self.channel)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'form': ChannelBannerForm(instance=self.banner),
            'banner': self.banner
        })

    def post(self, request, *args, **kwargs):
        uploaded_picture = request.FILES.get('original')
        cropX = int(float(request.POST.get('cropX')))
        cropY = int(float(request.POST.get('cropY')))
        cropWidth = int(float(request.POST.get('cropWidth')))
        cropHeight = int(float(request.POST.get('cropHeight')))

        if not os.path.exists(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}"):
            os.mkdir(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}")
        if not os.path.exists(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture"):
            os.mkdir(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture")
        if not os.path.exists(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/banner"):
            os.mkdir(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/banner")
        if not os.path.exists(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture/temp"):
            os.mkdir(f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/picture/temp")

        if not uploaded_picture and self.banner.original is None:
            return HttpResponseBadRequest()

        if self.banner.cropX != cropX:
            self.banner.cropX = cropX

        if self.banner.cropY != cropY:
            self.banner.cropY = cropY

        if self.banner.cropWidth != cropWidth:
            self.banner.cropWidth = cropWidth

        if self.banner.cropHeight != cropHeight:
            self.banner.cropHeight = cropHeight

        if self.banner.cropX != cropX or self.banner.cropY != cropY or self.banner.cropWidth != cropWidth or self.banner.cropHeight != cropHeight:
            self.banner.save()

        if uploaded_picture:
            picture_type = request.POST.get('type')
            picture_extension = picture_type.split('/')[-1]

            if self.banner.type != picture_type:
                self.banner.type = picture_type
                self.banner.save()

            self.banner.original.delete()
            self.banner.original.save(f"channel_banner.{picture_extension}", uploaded_picture)
        else:
            picture_extension = self.banner.type.split('/')[-1]

        original_url = f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/banner/temp/channel_banner.{picture_extension}"
        cropped_url = f"{settings.MEDIA_ROOT}/channels/{request.user.channel.uid}/banner/channel_banner.{picture_extension}"

        image = cv2.imread(original_url)
        cropped_img = image[cropY:cropY + cropHeight, cropX:cropX + cropWidth]
        cv2.imwrite(cropped_url, cropped_img)

        self.banner.cropped.delete()
        self.banner.cropped.save(f"channel_banner.{picture_extension}", File(open(cropped_url, 'rb')), save=False)
        self.banner.save()

        redirect_to = reverse('studio:customization', args=[self.channel.uid]) + '?section=branding'
        return HttpResponse(redirect_to)


class StudioCustomizationView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/customization/index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'customization'
        })


class LoadCustomizationBasicInfoView(LoginRequiredMixin, FormView):
    template_name = 'components/pages/studio/customization/_basic_info.html'
    form_class = ChannelBasicInfoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'instance': self.request.user.channel,
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect(self.request.user.channel.get_customization_url())


class LoadCustomizationBrandingView(LoginRequiredMixin, TemplateView):
    template_name = 'components/pages/studio/customization/_branding.html'


class LoadCustomizationLayoutView(LoginRequiredMixin, TemplateView):
    template_name = 'components/pages/studio/customization/_layout.html'


class LoadCustomizationLayoutTrailerView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/customization/layout/trailer.html'

    def get(self, request, *args, **kwargs):
        channel = request.user.channel
        videos = Video.objects.filter(author__channel=channel)
        paginator = Paginator(videos, 4)
        page = request.GET.get('page')
        query = None

        if 'search' in request.GET:
            query = request.GET.get('search')

            if query.strip() == '':
                results = videos
            else:
                results = videos.filter(title__icontains=query)
            paginator = Paginator(results, 4)

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context = {
            'videos': page_obj.object_list.all(),
            'query': query,
            'channel': channel,
            'trailer': channel.layout.trailer
        }

        if request.turbo.frame and request.turbo.has_turbo_header:
            return TurboStreamResponse([
                TurboStream("video-list-with-pagination").update.template("components/pages/studio/_trailer_videos_list.html", context).response(request).rendered_content
            ])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        channel = request.user.channel
        video_id = request.POST.get('video')
        context = {
            'channel': channel,
            'videos': Video.objects.filter(author__channel=channel)
        }
        if video_id:
            video = get_object_or_404(Video, id=video_id)
            ChannelLayout.objects.update(channel=channel, trailer=video)
            context.update({
                'trailer': video
            })

            return TurboStreamResponse([
                TurboStream(f"{request.turbo.frame}").update.template("pages/studio/customization/layout/trailer.html",
                                                                      context).response(request).rendered_content
            ])

        return self.render_to_response(context)


class LoadCustomizationLayoutTrailerPlayView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/customization/layout/trailer_play.html'

    def get(self, request, *args, **kwargs):
        channel = request.user.channel
        trailer = get_object_or_404(Video, uid=kwargs['trailer_uid'], author__channel=channel)

        return self.render_to_response({
            'video': trailer,
        })


class ChannelLinkOrderView(CsrfExemptMixin, JSONRequestResponseMixin, View):
    def post(self, request, channel_uid):
        channel = get_object_or_404(Channel, uid=channel_uid)

        for id, order in self.request_json.items():
            link = ChannelLink.objects.get(id=id, channel=channel)
            link.order = order
            link.save()

        return self.render_json_response({
            'saved': 'OK'
        })
