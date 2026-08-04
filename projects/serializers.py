from rest_framework import serializers
from .models import Project, Task , Tag

# ..........................................PROJECT SERIALIZER.............................................
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

# .........................................TAG SERIALIZER......................................





# ..........................................TASK SERIALIZER........................................
class TaskSerializer(serializers.ModelSerializer):

    subtasks = serializers.SerializerMethodField()


    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'parent_task', 'subtasks', 'tag', 'project']


    def get_subtasks(self, obj):
        if obj.subtasks.exists():
            return TaskSerializer(obj.subtasks.all(), many=True).data
        return []

class TaskBatchSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        tasks = [Task(**items) for items in validated_data]
        Task.objects.bulk_create(tasks)

class BulkTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'is_completed',
            'parent_task',
            'tag',
            'project',
        ]
        list_serializer_class = TaskBatchSerializer
