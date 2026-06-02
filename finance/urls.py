from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReceiptViewSet, PaymentViewSet, FundAllocationViewSet, ApprovalWorkflowViewSet

router = DefaultRouter()
router.register('receipts', ReceiptViewSet)
router.register('payments', PaymentViewSet)
router.register('fund-allocations', FundAllocationViewSet)
router.register('approvals', ApprovalWorkflowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
