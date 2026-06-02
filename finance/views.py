from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Receipt, Payment, FundAllocation, ApprovalWorkflow
from .serializers import (
    ReceiptSerializer, PaymentSerializer, FundAllocationSerializer, ApprovalWorkflowSerializer,
)


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['receipt_type', 'donation__donor', 'issued_by']
    ordering_fields = ['issue_date', 'created_at']

    def perform_create(self, serializer):
        receipt_number = Receipt.generate_receipt_number()
        serializer.save(issued_by=self.request.user, receipt_number=receipt_number)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['donation', 'payment_mode', 'status']
    ordering_fields = ['payment_date', 'amount']

    def perform_create(self, serializer):
        serializer.save()


class FundAllocationViewSet(viewsets.ModelViewSet):
    queryset = FundAllocation.objects.all()
    serializer_class = FundAllocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment', 'fund_type', 'department']


class ApprovalWorkflowViewSet(viewsets.ModelViewSet):
    queryset = ApprovalWorkflow.objects.all()
    serializer_class = ApprovalWorkflowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['entity_type', 'status', 'requested_by', 'reviewed_by']

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

