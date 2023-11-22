from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class StudioCopyrightView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/copyright.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'copyright'
        })
