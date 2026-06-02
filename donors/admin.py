from django.contrib import admin
from .models import Donor, DonorDocument, DonorEngagement


class DonorDocumentInline(admin.TabularInline):
    model = DonorDocument
    extra = 0


class DonorEngagementInline(admin.TabularInline):
    model = DonorEngagement
    extra = 0
    fields = ('engagement_type', 'subject', 'engagement_date', 'outcome')


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'donor_type', 'email', 'phone', 'city', 'account_manager', 'is_active', 'created_at')
    list_filter = ('donor_type', 'is_active', 'city', 'country')
    search_fields = ('first_name', 'last_name', 'organization_name', 'email', 'phone', 'cnic')
    inlines = [DonorDocumentInline, DonorEngagementInline]
    raw_id_fields = ('account_manager',)
    date_hierarchy = 'created_at'


@admin.register(DonorDocument)
class DonorDocumentAdmin(admin.ModelAdmin):
    list_display = ('donor', 'doc_type', 'title', 'uploaded_by', 'created_at')
    list_filter = ('doc_type',)
    search_fields = ('title', 'donor__first_name', 'donor__last_name', 'donor__organization_name')


@admin.register(DonorEngagement)
class DonorEngagementAdmin(admin.ModelAdmin):
    list_display = ('donor', 'engagement_type', 'subject', 'engagement_date', 'created_by')
    list_filter = ('engagement_type',)
    search_fields = ('subject', 'donor__first_name', 'donor__last_name')
    date_hierarchy = 'engagement_date'

