from django.test import TestCase
from django.contrib.auth.models import User
from donors.models import Donor, DonorDocument, DonorEngagement
from django.utils import timezone


class DonorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.donor = Donor.objects.create(
            donor_type='individual',
            first_name='Ali',
            last_name='Hassan',
            email='ali@example.com',
            phone='0300-1234567',
            city='Karachi',
            account_manager=self.user,
        )

    def test_donor_str_individual(self):
        self.assertEqual(str(self.donor), 'Ali Hassan')

    def test_donor_str_organization(self):
        corp = Donor.objects.create(
            donor_type='corporate',
            organization_name='ABC Corp',
            email='abc@corp.com',
        )
        self.assertEqual(str(corp), 'ABC Corp')

    def test_donor_str_email_fallback(self):
        d = Donor.objects.create(email='noname@example.com')
        self.assertEqual(str(d), 'noname@example.com')

    def test_donor_display_name(self):
        self.assertEqual(self.donor.display_name, 'Ali Hassan')

    def test_donor_is_active_default(self):
        self.assertTrue(self.donor.is_active)

    def test_donor_default_country(self):
        self.assertEqual(self.donor.country, 'Pakistan')


class DonorDocumentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='docuser', password='pass')
        self.donor = Donor.objects.create(email='donor@test.com')

    def test_document_str(self):
        doc = DonorDocument.objects.create(
            donor=self.donor,
            doc_type='mou',
            title='MoU Agreement',
            file='donor_documents/test.pdf',
            uploaded_by=self.user,
        )
        self.assertIn('MoU Agreement', str(doc))


class DonorEngagementTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='enguser', password='pass')
        self.donor = Donor.objects.create(email='eng@test.com')

    def test_engagement_str(self):
        eng = DonorEngagement.objects.create(
            donor=self.donor,
            engagement_type='meeting',
            subject='Initial Meeting',
            engagement_date=timezone.now(),
            created_by=self.user,
        )
        self.assertIn('meeting', str(eng))
        self.assertIn(str(self.donor), str(eng))

