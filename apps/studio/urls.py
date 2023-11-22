from django.urls import path, include
from apps.studio import views


app_name = 'studio'

urlpatterns = [
    path("create-channel/", views.ChannelCreationView.as_view(), name="create-channel"),

    path('<channel_uid>/customization/', include('apps.studio.customization.urls')),
    path('<channel_uid>/analytics/', include('apps.studio.analytics.urls')),
    path('<channel_uid>/comments/', include('apps.studio.comments.urls')),
    path('<channel_uid>/contents/', include('apps.studio.contents.urls')),
    path('<channel_uid>/videos/<video_id>/', include('apps.studio.videos.urls')),
    path('<channel_uid>/subtitles/', include('apps.studio.subtitles.urls')),
    path('<channel_uid>/dashboard/', include('apps.studio.dashboard.urls')),
    path('<channel_uid>/upload/', include('apps.studio.upload.urls')),
    path('<channel_uid>/copyright/', include('apps.studio.copyright.urls')),
    path('<channel_uid>/earn/', include('apps.studio.earn.urls')),
    path('<channel_uid>/audio-library/', include('apps.studio.library.urls')),
]
