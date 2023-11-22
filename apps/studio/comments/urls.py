from django.urls import path
from apps.studio.comments import views


urlpatterns = [
    path('', views.StudioCommentsView.as_view(), name='comments'),
    path('lists/', views.LoadCommentsView.as_view(), name='comments-list'),
]
