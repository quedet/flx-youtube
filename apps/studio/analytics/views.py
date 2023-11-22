from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class StudioAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/studio/analytics/index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'page': 'analytics'
        })
