from django.contrib import admin
from .models import Campaign, Pledge, Donation, Event, EventParticipant


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign_type', 'goal_amount', 'start_date', 'end_date', 'status', 'owner')
    list_filter = ('status', 'campaign_type')
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('donor', 'campaign', 'amount', 'status', 'pledge_date', 'due_date')
    list_filter = ('status', 'campaign')
    search_fields = ('donor__first_name', 'donor__last_name', 'donor__organization_name')
    date_hierarchy = 'pledge_date'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'campaign', 'amount', 'donation_date', 'pledge')
    list_filter = ('campaign', 'donation_date')
    search_fields = ('donor__first_name', 'donor__last_name', 'purpose')
    date_hierarchy = 'donation_date'


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'event_date', 'venue', 'status', 'target_attendees')
    list_filter = ('status', 'campaign')
    search_fields = ('name', 'venue')
    inlines = [EventParticipantInline]

