from rest_framework import serializers
from .models import Receipt, Payment, FundAllocation, ApprovalWorkflow


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ('receipt_number', 'issue_date', 'created_at')


class FundAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundAllocation
        fields = '__all__'
        read_only_fields = ('created_at',)


class PaymentSerializer(serializers.ModelSerializer):
    allocations = FundAllocationSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = '__all__'
        read_only_fields = ('created_at', 'reviewed_at')
