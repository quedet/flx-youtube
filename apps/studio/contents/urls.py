from django.urls import path
from apps.studio.contents import views


urlpatterns = [
    path('', views.StudioContentView.as_view(), name='content'),
    path('videos/', views.LoadStudioVideosContentView.as_view(), name='content-videos'),
    path('lives/', views.LoadStudioLiveContentView.as_view(), name='content-lives'),
    path('podcasts/', views.LoadStudioPodcastsContentView.as_view(), name='content-podcasts'),
    path('playlists/', views.LoadStudioPlaylistsContentView.as_view(), name='content-playlists'),
    path('playlists/add/', views.StudioPlaylistCreationView.as_view(), name='content-playlists-creation'),
    path('promotions/', views.LoadStudioPromotionsContentView.as_view(), name='content-promotions'),
]
