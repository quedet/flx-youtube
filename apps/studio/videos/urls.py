from django.urls import path
from apps.studio.videos import views

urlpatterns = [
    path('', views.StudioVideoDetailsView.as_view(), name='video-detail'),
    path('topics/', views.StudioVideoTopicsSearchView.as_view(), name='video-topics'),
    path('analytics/', views.StudioVideoAnalyticsView.as_view(), name='video-analytics'),
    path('comments/', views.StudioVideoCommentsView.as_view(), name='video-comments'),
    path('comments/api/fetch/', views.StudioVideoFetchCommentsView.as_view(), name='video-comments-fetch'),
    path('editor/', views.StudioVideoEditorView.as_view(), name='video-editor'),
]
