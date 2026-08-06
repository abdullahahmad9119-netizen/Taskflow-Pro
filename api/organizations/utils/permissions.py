from rest_framework.permissions import BasePermission

class IsOrganizationMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.memberships.filter(user=request.user).exists()