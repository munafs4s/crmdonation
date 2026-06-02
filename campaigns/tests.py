from django.test import TestCase
from django.contrib.auth.models import User
from donors.models import Donor
from campaigns.models import Campaign, Pledge, Donation, Event, EventParticipant
from django.utils import timezone
import datetime


class CampaignModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='camuser', password='pass')
        self.campaign = Campaign.objects.create(
            name='Annual Fundraiser 2024',
            campaign_type='general',
            goal_amount=1000000,
            start_date=datetime.date.today(),
            status='active',
            owner=self.user,
        )

    def test_campaign_str(self):
        self.assertEqual(str(self.campaign), 'Annual Fundraiser 2024')

    def test_campaign_default_status(self):
        c = Campaign.objects.create(
            name='Test Campaign',
            start_date=datetime.date.today(),
        )
        self.assertEqual(c.status, 'planning')


class PledgeModelTest(TestCase):
    def setUp(self):
        self.donor = Donor.objects.create(email='pledge@test.com')
        self.campaign = Campaign.objects.create(
            name='Pledge Campaign',
            start_date=datetime.date.today(),
        )
        self.pledge = Pledge.objects.create(
            donor=self.donor,
            campaign=self.campaign,
            amount=50000,
            pledge_date=datetime.date.today(),
        )

    def test_pledge_str(self):
        self.assertIn('50000', str(self.pledge))
        self.assertIn('pending', str(self.pledge))

    def test_pledge_default_status(self):
        self.assertEqual(self.pledge.status, 'pending')

    def test_pledge_amount_outstanding_no_payments(self):
        self.assertEqual(self.pledge.amount_outstanding, 50000)


class DonationModelTest(TestCase):
    def setUp(self):
        self.donor = Donor.objects.create(email='donation@test.com')
        self.campaign = Campaign.objects.create(
            name='Donation Campaign',
            start_date=datetime.date.today(),
        )

    def test_donation_str(self):
        donation = Donation.objects.create(
            donor=self.donor,
            campaign=self.campaign,
            amount=5000,
            donation_date=datetime.date.today(),
        )
        self.assertIn('5000', str(donation))


class EventModelTest(TestCase):
    def setUp(self):
        self.campaign = Campaign.objects.create(
            name='Event Campaign',
            start_date=datetime.date.today(),
        )

    def test_event_str(self):
        event = Event.objects.create(
            name='Gala Dinner',
            event_date=timezone.now(),
            campaign=self.campaign,
        )
        self.assertEqual(str(event), 'Gala Dinner')

    def test_event_participant_str(self):
        donor = Donor.objects.create(email='attendee@test.com')
        event = Event.objects.create(name='Test Event', event_date=timezone.now())
        ep = EventParticipant.objects.create(event=event, donor=donor)
        self.assertIn(str(donor), str(ep))
        self.assertIn(str(event), str(ep))

