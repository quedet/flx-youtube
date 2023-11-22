from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class StudioSubtitlesView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/subtitles.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'subtitles'
        })
