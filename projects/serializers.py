from rest_framework import serializers
from .models import Project
class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'descriptions',
            'status',
            'priority',
            'created_at',
            'ís_archived',
            'organization',
            'created_by'
        )
        read_only_fields = ('id', 'organization', 'created_at', 'created_by')
