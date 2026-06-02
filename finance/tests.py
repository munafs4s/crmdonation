from django.test import TestCase
from django.contrib.auth.models import User
from donors.models import Donor
from campaigns.models import Campaign, Pledge, Donation
from finance.models import Receipt, Payment, FundAllocation, ApprovalWorkflow
import datetime


class ReceiptModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='finuser', password='pass')
        self.donor = Donor.objects.create(email='fin@test.com')
        self.campaign = Campaign.objects.create(
            name='Finance Test Campaign',
            start_date=datetime.date.today(),
        )
        self.pledge = Pledge.objects.create(
            donor=self.donor,
            campaign=self.campaign,
            amount=10000,
            pledge_date=datetime.date.today(),
        )
        self.donation = Donation.objects.create(
            donor=self.donor,
            campaign=self.campaign,
            pledge=self.pledge,
            amount=10000,
            donation_date=datetime.date.today(),
        )

    def test_receipt_number_generation(self):
        rn = Receipt.generate_receipt_number()
        self.assertTrue(rn.startswith('RCP-'))

    def test_receipt_number_sequential(self):
        rn1 = Receipt.generate_receipt_number()
        Receipt.objects.create(
            donation=self.donation,
            receipt_number=rn1,
            issued_by=self.user,
        )
        rn2 = Receipt.generate_receipt_number()
        seq1 = int(rn1.split('-')[-1])
        seq2 = int(rn2.split('-')[-1])
        self.assertEqual(seq2, seq1 + 1)

    def test_receipt_str(self):
        rn = Receipt.generate_receipt_number()
        receipt = Receipt.objects.create(
            donation=self.donation,
            receipt_number=rn,
            issued_by=self.user,
        )
        self.assertIn(rn, str(receipt))


class PaymentModelTest(TestCase):
    def setUp(self):
        self.donor = Donor.objects.create(email='pay@test.com')
        self.campaign = Campaign.objects.create(
            name='Payment Campaign',
            start_date=datetime.date.today(),
        )
        self.donation = Donation.objects.create(
            donor=self.donor,
            campaign=self.campaign,
            amount=5000,
            donation_date=datetime.date.today(),
        )

    def test_payment_str(self):
        payment = Payment.objects.create(
            donation=self.donation,
            amount=5000,
            payment_mode='bank_transfer',
            payment_date=datetime.date.today(),
        )
        self.assertIn('5000', str(payment))
        self.assertIn('bank_transfer', str(payment))

    def test_payment_default_status(self):
        payment = Payment.objects.create(
            donation=self.donation,
            amount=5000,
            payment_mode='cash',
            payment_date=datetime.date.today(),
        )
        self.assertEqual(payment.status, 'pending')


class FundAllocationTest(TestCase):
    def setUp(self):
        self.donor = Donor.objects.create(email='alloc@test.com')
        self.campaign = Campaign.objects.create(
            name='Alloc Campaign',
            start_date=datetime.date.today(),
        )
        self.donation = Donation.objects.create(
            donor=self.donor,
            campaign=self.campaign,
            amount=10000,
            donation_date=datetime.date.today(),
        )
        self.payment = Payment.objects.create(
            donation=self.donation,
            amount=10000,
            payment_mode='cash',
            payment_date=datetime.date.today(),
        )

    def test_fund_allocation_str(self):
        fa = FundAllocation.objects.create(
            payment=self.payment,
            fund_type='restricted',
            department='Cardiology',
            amount=10000,
        )
        self.assertIn('restricted', str(fa))
        self.assertIn('Cardiology', str(fa))

