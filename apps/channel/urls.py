from django.urls import path
from . import views

app_name = "channel"

urlpatterns = [
    path("fetch/channel/<channel_slug>", views.FetchChannelVideosView.as_view(), name="fetch-channel-videos"),

    path("@<channel_pseudo>/", views.ChannelHomeView.as_view(), name='home'),
    path("@<channel_code__name>/about/", views.ChannelAboutView.as_view(), name='about'),
    path("@<channel_code__name>/videos/", views.ChannelVideosView.as_view(), name='videos'),
    path("@<channel_code__name>/playlists/", views.ChannelPlaylistsView.as_view(), name='playlists'),
    path("@<channel_code__name>/community/", views.ChannelCommunityView.as_view(), name='community'),
]