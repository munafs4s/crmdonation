from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Campaign, Pledge, Donation, Event, EventParticipant
from .serializers import (
    CampaignSerializer, PledgeSerializer, DonationSerializer,
    EventSerializer, EventParticipantSerializer,
)


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'campaign_type', 'owner']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'goal_amount']


class PledgeViewSet(viewsets.ModelViewSet):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['donor', 'campaign', 'status']
    ordering_fields = ['pledge_date', 'due_date', 'amount']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['donor', 'campaign', 'pledge']
    ordering_fields = ['donation_date', 'amount']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'campaign']
    search_fields = ['name', 'description', 'venue']


class EventParticipantViewSet(viewsets.ModelViewSet):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'donor', 'attended']

