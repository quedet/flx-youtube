from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class StudioEarnView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/earn.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'earn'
        })

