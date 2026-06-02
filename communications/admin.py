from django.contrib import admin
from .models import EmailTemplate, CommunicationLog, BulkCommunication


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'subject', 'created_by', 'created_at')
    list_filter = ('template_type',)
    search_fields = ('name', 'subject')


@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = ('donor', 'channel', 'subject', 'status', 'sent_by', 'sent_at')
    list_filter = ('channel', 'status')
    search_fields = ('donor__first_name', 'donor__last_name', 'subject')
    date_hierarchy = 'sent_at'


@admin.register(BulkCommunication)
class BulkCommunicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel', 'status', 'sent_by', 'scheduled_at', 'sent_at')
    list_filter = ('channel', 'status')
    search_fields = ('name', 'subject')
    filter_horizontal = ('recipients',)

