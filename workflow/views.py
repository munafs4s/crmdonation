from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Reminder
from .serializers import TaskSerializer, ReminderSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['task_type', 'status', 'priority', 'assigned_to', 'donor']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['reminder_type', 'sent', 'donor', 'task']
    ordering_fields = ['remind_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

