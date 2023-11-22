from django.urls import path, re_path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="index"),
    path("results/", views.VideoSearchIndexView.as_view(), name="search"),
    path("api/search/results/", views.VideoSearchResultsView.as_view(), name="search-results"),
    path("fetcher", views.VideoFetcherView.as_view(), name="fetcher"),
    path("fetch/<uid>/related/", views.FetchRelatedVideoView.as_view(), name="fetch-related"),
    path("fetch/<uid>/comments/", views.FetchVideoCommentView.as_view(), name="fetch-comments"),
    path("fetch/<uid>/comments/<comment_id>/replies/", views.FetchVideoCommentReplyView.as_view(), name="fetch-replies"),
    path("watch", views.DetailView.as_view(), name="detail"),
]