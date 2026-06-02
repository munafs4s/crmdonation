from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from donors.models import Donor
import datetime


class DonorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.client.force_authenticate(user=self.user)
        self.donor = Donor.objects.create(
            first_name='Sara',
            last_name='Ahmed',
            email='sara@test.com',
            donor_type='individual',
        )

    def test_list_donors(self):
        response = self.client.get('/api/donors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_retrieve_donor(self):
        response = self.client.get(f'/api/donors/{self.donor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'sara@test.com')

    def test_create_donor(self):
        data = {
            'first_name': 'Omar',
            'last_name': 'Khan',
            'email': 'omar@test.com',
            'donor_type': 'hni',
            'phone': '0321-9876543',
        }
        response = self.client.post('/api/donors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'omar@test.com')

    def test_update_donor(self):
        data = {'email': 'sara.updated@test.com', 'first_name': 'Sara', 'last_name': 'Ahmed'}
        response = self.client.patch(f'/api/donors/{self.donor.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'sara.updated@test.com')

    def test_delete_donor(self):
        response = self.client.delete(f'/api/donors/{self.donor.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        unauth_client = APIClient()
        response = unauth_client.get('/api/donors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_donor(self):
        response = self.client.get('/api/donors/?search=Sara')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)


class CampaignAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='campuser', password='pass')
        self.client.force_authenticate(user=self.user)

    def test_create_campaign(self):
        data = {
            'name': 'Zakat Drive 2024',
            'campaign_type': 'zakat',
            'goal_amount': '500000.00',
            'start_date': str(datetime.date.today()),
            'status': 'active',
        }
        response = self.client.post('/api/campaigns/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Zakat Drive 2024')

    def test_list_campaigns(self):
        response = self.client.get('/api/campaigns/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DashboardReportTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='rptuser', password='pass')
        self.client.force_authenticate(user=self.user)

    def test_dashboard_summary(self):
        response = self.client.get('/api/reports/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_active_donors', response.data)
        self.assertIn('total_raised', response.data)

    def test_donor_retention(self):
        response = self.client.get('/api/reports/donor-retention/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('retention_rate', response.data)

    def test_financial_reconciliation(self):
        response = self.client.get('/api/reports/financial-reconciliation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('by_payment_mode', response.data)

