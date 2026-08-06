from rest_framework import serializers
from logs.models import Timelog

class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timelog
        fields = ("id", "task", "user", "hours_spent", "work_date", "created_at")
        read_only_fields = ("user","created_at")