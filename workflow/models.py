from django.db import models
from django.contrib.auth.models import User
from donors.models import Donor


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    TASK_TYPE_CHOICES = [
        ('follow_up', 'Follow-Up'),
        ('pledge_reminder', 'Pledge Reminder'),
        ('meeting', 'Meeting'),
        ('call', 'Call'),
        ('approval', 'Approval'),
        ('payment_reminder', 'Payment Reminder'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    task_type = models.CharField(max_length=30, choices=TASK_TYPE_CHOICES, default='other')
    description = models.TextField(blank=True)
    donor = models.ForeignKey(
        Donor, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_tasks'
    )
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_tasks'
    )
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date', '-priority']

    def __str__(self):
        return self.title


class Reminder(models.Model):
    REMINDER_TYPE_CHOICES = [
        ('pledge_due', 'Pledge Due'),
        ('follow_up', 'Follow-Up'),
        ('meeting', 'Meeting'),
        ('recurring_donor', 'Recurring Donor Alert'),
        ('payment_pending', 'Payment Pending'),
        ('custom', 'Custom'),
    ]

    task = models.ForeignKey(
        Task, null=True, blank=True, on_delete=models.CASCADE, related_name='reminders'
    )
    reminder_type = models.CharField(max_length=30, choices=REMINDER_TYPE_CHOICES, default='custom')
    donor = models.ForeignKey(
        Donor, null=True, blank=True, on_delete=models.SET_NULL, related_name='reminders'
    )
    message = models.TextField()
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['remind_at']

    def __str__(self):
        return f"{self.reminder_type} at {self.remind_at}"

