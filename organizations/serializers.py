from rest_framework import serializers
from .models import Organization,Membership

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('role', 'organizations', 'user', 'joined_at')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'slug', 'owner', 'created_at')
        read_only_fields = ('slug', 'owner', 'created_at')