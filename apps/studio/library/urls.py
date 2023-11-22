from django.urls import path
from apps.studio.library import views


urlpatterns = [
    path('', views.StudioAudioLibraryView.as_view(), name='audio-library')
]
