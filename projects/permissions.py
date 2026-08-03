from rest_framework.permissions import BasePermission
from organizations.models import Membership

class IsProjectManagerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        org = obj.organization

        try:
            membership = Membership.objects.get(
                user = request.user, organization=org
            )
        except Membership.DoesNotExists:
            return False

        if request.method in ['GET','OPTIONS', 'HEAD']:
            return membership.role in ["MEMBER", "MANAGER","ADMIN"]
        return membership.role in ["MANAGER", "ADMIN"]

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True