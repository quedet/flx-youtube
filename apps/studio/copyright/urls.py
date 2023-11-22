from django.urls import path
from apps.studio.copyright import views


urlpatterns = [
    path('', views.StudioCopyrightView.as_view(), name='copyright')
]
