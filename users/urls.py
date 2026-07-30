from django.urls import path
from .views import RegisterView, PasswordChangeView,ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(),name="Register"),
    path("auth/login/", TokenObtainPairView.as_view(),name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(),name="refresh"),
    path("auth/change-password/", PasswordChangeView.as_view(),name="Change-password"),
    path("me/", ProfileView.as_view(), name="profile")
]