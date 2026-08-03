from rest_framework import serializers
from .models import Organization,Membership, Invitations

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('role', 'organizations', 'user', 'joined_at')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'slug', 'owner', 'created_at')
        read_only_fields = ('slug', 'owner', 'created_at')

class InvitaionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitations
        fields = ["email", "role"]

    def validate_email(self, value):

        org_id = self.context.get("org_id")
        if org_id:
            if Membership.objects.filter(
                organization_id = org_id,
                user__email = value
            ).exists():
                raise serializers.ValidationError("already a memeber of the organization")
            return value
