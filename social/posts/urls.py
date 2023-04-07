from django.urls import path

from posts.views import (
    UserPostView,
    LikeAnalyticsView,
    PostListView,
    PostDetailsView,
    LikeView
)

urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:post_id>/', PostDetailsView.as_view()),
    path('user_posts/', UserPostView.as_view()),
    path('<int:post_id>/like/', LikeView.as_view()),
    path('analytics/', LikeAnalyticsView.as_view()),
]
