from django.db import models
from django.contrib.auth.models import User
from donors.models import Donor


class EmailTemplate(models.Model):
    TEMPLATE_TYPE_CHOICES = [
        ('acknowledgement', 'Donation Acknowledgement'),
        ('pledge_reminder', 'Pledge Reminder'),
        ('event_invite', 'Event Invitation'),
        ('event_reminder', 'Event Reminder'),
        ('thank_you', 'Thank You'),
        ('newsletter', 'Newsletter'),
        ('zakat_receipt', 'Zakat Receipt'),
        ('custom', 'Custom'),
    ]

    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPE_CHOICES, default='custom')
    subject = models.CharField(max_length=300)
    body_html = models.TextField()
    body_text = models.TextField(blank=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CommunicationLog(models.Model):
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('call', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='communication_logs')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    template = models.ForeignKey(
        EmailTemplate, null=True, blank=True, on_delete=models.SET_NULL
    )
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    sent_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.donor} – {self.channel} on {self.sent_at.date()}"


class BulkCommunication(models.Model):
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=200)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='email')
    template = models.ForeignKey(
        EmailTemplate, null=True, blank=True, on_delete=models.SET_NULL
    )
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    recipients = models.ManyToManyField(Donor, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    sent_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.channel})"

