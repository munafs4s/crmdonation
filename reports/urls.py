from django.urls import path
from .views import DashboardSummaryView, CampaignPerformanceView, DonorRetentionView, FinancialReconciliationView

urlpatterns = [
    path('dashboard/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('campaign-performance/', CampaignPerformanceView.as_view(), name='campaign-performance'),
    path('donor-retention/', DonorRetentionView.as_view(), name='donor-retention'),
    path('financial-reconciliation/', FinancialReconciliationView.as_view(), name='financial-reconciliation'),
]
