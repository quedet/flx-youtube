from django.urls import path
from apps.studio.earn import views


urlpatterns = [
    path('', views.StudioEarnView.as_view(), name='earn'),
]
