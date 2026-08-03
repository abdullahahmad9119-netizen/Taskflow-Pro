from .views import (MembershipListCreateAPIView,
                    MembershipDetailView,
                    OrganizationDetailView,
                    OrganizationListCreateAPIview,
                    AcceptInvitationView,
                    ListInvitationsView,
                    CreateInvitationView,
                    DeleteReviewInvitationView)
from django.urls import path

urlpatterns = [
    path('organizations/', OrganizationListCreateAPIview.as_view(), name="organization-list-create"),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name="organization-details"),

    path('membership/', MembershipListCreateAPIView.as_view(), name="membership-list-create"),
    path('membership/<int:pk>/', MembershipDetailView.as_view(), name="membership-details"),

    path('organization/<int:org_id>/invites/creates/', CreateInvitationView.as_view(), name="create-invitation"),
    path('invitations/accept/<uuid:token>/', AcceptInvitationView.as_view(), name="Accept-invite"),
    path('organization/<int:org_id>/invites', ListInvitationsView.as_view(), name="list-invitations"),
    path('invitations/<int:invite_id>/revoke', DeleteReviewInvitationView.as_view(), name="delete-invite")
]