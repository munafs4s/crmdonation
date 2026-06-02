from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import EmailTemplate, CommunicationLog, BulkCommunication
from .serializers import EmailTemplateSerializer, CommunicationLogSerializer, BulkCommunicationSerializer


class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['template_type']
    search_fields = ['name', 'subject']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommunicationLogViewSet(viewsets.ModelViewSet):
    queryset = CommunicationLog.objects.all()
    serializer_class = CommunicationLogSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['donor', 'channel', 'status']
    ordering_fields = ['sent_at']

    def perform_create(self, serializer):
        serializer.save(sent_by=self.request.user)


class BulkCommunicationViewSet(viewsets.ModelViewSet):
    queryset = BulkCommunication.objects.all()
    serializer_class = BulkCommunicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['channel', 'status']
    search_fields = ['name', 'subject']

    def perform_create(self, serializer):
        serializer.save(sent_by=self.request.user)

