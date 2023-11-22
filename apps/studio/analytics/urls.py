from django.urls import path
from apps.studio.analytics import views


urlpatterns = [
    path('', views.StudioAnalyticsView.as_view(), name='analytics'),
]
