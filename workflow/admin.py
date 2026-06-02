from django.contrib import admin
from .models import Task, Reminder


class ReminderInline(admin.TabularInline):
    model = Reminder
    extra = 0
    fields = ('reminder_type', 'message', 'remind_at', 'sent')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'priority', 'status', 'assigned_to', 'due_date', 'donor')
    list_filter = ('task_type', 'status', 'priority')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
    inlines = [ReminderInline]


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('reminder_type', 'donor', 'remind_at', 'sent', 'created_by')
    list_filter = ('reminder_type', 'sent')
    date_hierarchy = 'remind_at'

