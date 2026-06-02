from rest_framework import serializers
from .models import Task, Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at')


class TaskSerializer(serializers.ModelSerializer):
    reminders = ReminderSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'completed_at')
