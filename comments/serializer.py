from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'parent_comment', 'body', 'created_at', 'updated_at', 'replies']
        read_only_fields= ["author", "created_at", "updated_at"]
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)