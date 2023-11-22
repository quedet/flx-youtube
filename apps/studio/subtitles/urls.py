from django.urls import path
from apps.studio.subtitles import views

urlpatterns = [
    path('', views.StudioSubtitlesView.as_view(), name='subtitles')
]
