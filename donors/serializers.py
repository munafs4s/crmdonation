from rest_framework import serializers
from .models import Donor, DonorDocument, DonorEngagement


class DonorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorDocument
        fields = '__all__'
        read_only_fields = ('uploaded_by',)


class DonorEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorEngagement
        fields = '__all__'
        read_only_fields = ('created_by',)


class DonorSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField()
    documents = DonorDocumentSerializer(many=True, read_only=True)
    engagements = DonorEngagementSerializer(many=True, read_only=True)

    class Meta:
        model = Donor
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class DonorListSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField()

    class Meta:
        model = Donor
        fields = (
            'id', 'display_name', 'donor_type', 'email', 'phone',
            'city', 'account_manager', 'is_active', 'created_at',
        )
