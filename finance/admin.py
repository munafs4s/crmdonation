from django.contrib import admin
from .models import Receipt, Payment, FundAllocation, ApprovalWorkflow


class FundAllocationInline(admin.TabularInline):
    model = FundAllocation
    extra = 0


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'donation', 'receipt_type', 'issue_date', 'issued_by')
    list_filter = ('receipt_type',)
    search_fields = ('receipt_number', 'donation__donor__first_name', 'donation__donor__organization_name')
    date_hierarchy = 'issue_date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('donation', 'amount', 'payment_mode', 'status', 'payment_date', 'verified_by')
    list_filter = ('payment_mode', 'status')
    search_fields = ('transaction_ref', 'cheque_number', 'donation__donor__first_name')
    date_hierarchy = 'payment_date'
    inlines = [FundAllocationInline]


@admin.register(FundAllocation)
class FundAllocationAdmin(admin.ModelAdmin):
    list_display = ('payment', 'fund_type', 'department', 'campaign_label', 'amount')
    list_filter = ('fund_type',)


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'entity_id', 'status', 'requested_by', 'reviewed_by', 'created_at')
    list_filter = ('entity_type', 'status')
    date_hierarchy = 'created_at'

