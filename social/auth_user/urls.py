from auth_user.views import (UserCreateView, UserLoginView, UserLogoutView, UserAnalyticsView)
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', UserCreateView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('<int:user_id>/analytics/', UserAnalyticsView.as_view())
]
