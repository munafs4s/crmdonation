from django.db import models
from django.contrib.auth.models import User
from campaigns.models import Donation


class Receipt(models.Model):
    RECEIPT_TYPE_CHOICES = [
        ('general', 'General Donation'),
        ('zakat', 'Zakat'),
        ('sadaqah', 'Sadaqah'),
        ('sponsorship', 'Sponsorship'),
        ('csr', 'CSR'),
    ]

    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True)
    receipt_type = models.CharField(max_length=20, choices=RECEIPT_TYPE_CHOICES, default='general')
    issue_date = models.DateField(auto_now_add=True)
    zakat_declaration = models.TextField(blank=True)
    issued_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Receipt #{self.receipt_number} – {self.donation}"

    @classmethod
    def generate_receipt_number(cls):
        from django.utils import timezone
        year = timezone.now().year
        last = cls.objects.filter(receipt_number__startswith=f'RCP-{year}-').order_by('-receipt_number').first()
        if last:
            seq = int(last.receipt_number.split('-')[-1]) + 1
        else:
            seq = 1
        return f"RCP-{year}-{seq:05d}"


class Payment(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment Gateway'),
        ('pos', 'POS / Card Transaction'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_ref = models.CharField(max_length=100, blank=True)
    cheque_number = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    payment_date = models.DateField()
    notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='verified_payments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.donation.donor} – PKR {self.amount} via {self.payment_mode}"


class FundAllocation(models.Model):
    FUND_TYPE_CHOICES = [
        ('restricted', 'Restricted'),
        ('unrestricted', 'Unrestricted'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='allocations')
    fund_type = models.CharField(max_length=20, choices=FUND_TYPE_CHOICES, default='unrestricted')
    department = models.CharField(max_length=200, blank=True)
    campaign_label = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fund_type} – {self.department or self.campaign_label} – PKR {self.amount}"


class ApprovalWorkflow(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    ENTITY_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('receipt', 'Receipt'),
        ('pledge', 'Pledge'),
    ]

    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.PositiveIntegerField()
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='approval_requests'
    )
    reviewed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approval_reviews'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.entity_type} #{self.entity_id} – {self.status}"

