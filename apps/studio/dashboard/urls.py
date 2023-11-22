from django.urls import path, include
from apps.studio.dashboard import views

urlpatterns = [
    path('', views.StudioDashboardView.as_view(), name='dashboard'),
]
