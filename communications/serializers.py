from rest_framework import serializers
from .models import EmailTemplate, CommunicationLog, BulkCommunication


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CommunicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationLog
        fields = '__all__'
        read_only_fields = ('sent_at',)


class BulkCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkCommunication
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at')
