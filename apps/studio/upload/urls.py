from django.urls import path
from apps.studio.upload import views


urlpatterns = [
    path('', views.StudioUploadView.as_view(), name='upload'),
    path('<draft_id>/topics/', views.StudioDraftTopicsSearchView.as_view(), name='draft-topics'),
    path('<draft_id>/', views.StudioDraftUpdateView.as_view(), name='update'),
    path('<draft_id>/generate-thumbnails/', views.GenerateVideosThumbnailsView.as_view(), name='generate-thumbnails'),
    path('<draft_id>/publish', views.StudioPublishingView.as_view(), name='publish')
]
