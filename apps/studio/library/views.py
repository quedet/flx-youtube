from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class StudioAudioLibraryView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/audio_library.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'audio'
        })


