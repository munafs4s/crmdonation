from django.db import models
from django.contrib.auth.models import User


class Donor(models.Model):
    DONOR_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('corporate', 'Corporate Partner'),
        ('csr', 'CSR Contributor'),
        ('foundation', 'Foundation / Trust'),
        ('welfare', 'Welfare / Zakat Donor'),
        ('event_sponsor', 'Event Sponsor / Participant'),
        ('hni', 'High-Net-Worth Individual'),
        ('vendor', 'Vendor / Strategic Partner'),
    ]

    donor_type = models.CharField(max_length=30, choices=DONOR_TYPE_CHOICES, default='individual')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    organization_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Pakistan')
    cnic = models.CharField(max_length=20, blank=True, verbose_name='CNIC / NTN')
    preferred_causes = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    account_manager = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='managed_donors'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.organization_name:
            return self.organization_name
        return f"{self.first_name} {self.last_name}".strip() or self.email

    @property
    def display_name(self):
        return str(self)


class DonorDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('mou', 'MoU'),
        ('proposal', 'Proposal'),
        ('agreement', 'Agreement'),
        ('receipt', 'Receipt'),
        ('other', 'Other'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default='other')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='donor_documents/')
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor} – {self.title}"


class DonorEngagement(models.Model):
    ENGAGEMENT_TYPE_CHOICES = [
        ('meeting', 'Meeting'),
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('event', 'Event'),
        ('other', 'Other'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='engagements')
    engagement_type = models.CharField(max_length=20, choices=ENGAGEMENT_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    engagement_date = models.DateTimeField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-engagement_date']

    def __str__(self):
        return f"{self.donor} – {self.engagement_type} on {self.engagement_date.date()}"

