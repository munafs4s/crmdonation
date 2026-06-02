from rest_framework import serializers
from .models import Campaign, Pledge, Donation, Event, EventParticipant


class CampaignSerializer(serializers.ModelSerializer):
    total_raised = serializers.ReadOnlyField()

    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PledgeSerializer(serializers.ModelSerializer):
    amount_paid = serializers.ReadOnlyField()
    amount_outstanding = serializers.ReadOnlyField()

    class Meta:
        model = Pledge
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ('created_at',)


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    participants = EventParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at',)
