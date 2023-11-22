import http

from django.shortcuts import reverse, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.channel.models import Channel
from apps.studio.forms import ChannelCreationForm


class ChannelCreationView(LoginRequiredMixin, FormView):
    template_name = 'pages/registration/channel/creation.html'
    form_class = ChannelCreationForm

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            channel = user.channel
            return redirect(reverse('channel:home', args=[channel.pseudo]))
        except Exception:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        channel = Channel.objects.create(author=self.request.user, **form.cleaned_data)
        redirect_to = reverse('studio:customization', args=[channel.uid]) + '?section=branding'
        return redirect(redirect_to)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response
