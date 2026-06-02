from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Donor, DonorDocument, DonorEngagement
from .serializers import DonorSerializer, DonorListSerializer, DonorDocumentSerializer, DonorEngagementSerializer


class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['donor_type', 'is_active', 'account_manager', 'city']
    search_fields = ['first_name', 'last_name', 'organization_name', 'email', 'phone']
    ordering_fields = ['created_at', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return DonorListSerializer
        return DonorSerializer

    def get_queryset(self):
        return Donor.objects.select_related('account_manager').prefetch_related(
            'documents', 'engagements'
        )


class DonorDocumentViewSet(viewsets.ModelViewSet):
    queryset = DonorDocument.objects.all()
    serializer_class = DonorDocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['donor', 'doc_type']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class DonorEngagementViewSet(viewsets.ModelViewSet):
    queryset = DonorEngagement.objects.all()
    serializer_class = DonorEngagementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['donor', 'engagement_type']
    ordering_fields = ['engagement_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

