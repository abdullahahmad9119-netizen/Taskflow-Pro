from .views import (MembershipListCreateAPIView,
                    MembershipDetailView,
                    OrganizationDetailView,
                    OrganizationListCreateAPIview)
from django.urls import path

urlpatterns = [
    path('organizations/', OrganizationListCreateAPIview.as_view(), name="organization-list-create"),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name="organization-details"),

    path('membership/', MembershipListCreateAPIView.as_view(), name="membership-list-create"),
    path('membership/<int:pk>/', MembershipDetailView.as_view(), name="membership-details")
]