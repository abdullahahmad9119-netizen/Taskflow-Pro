from django.urls import path
from .views import RegisterView, PasswordChangeView,ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(),name="Register"),
    path("auth/login/", TokenObtainPairView.as_view(),name="Register"),
    path("auth/refresh/", TokenRefreshView.as_view(),name="Register"),
    path("auth/change-password/", PasswordChangeView.as_view(),name="Register"),
    path("me/", ProfileView.as_view(), name="profile")
]