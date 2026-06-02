from django.db import models
from django.contrib.auth.models import User
from donors.models import Donor


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    CAMPAIGN_TYPE_CHOICES = [
        ('general', 'General Fundraising'),
        ('zakat', 'Zakat Campaign'),
        ('csr', 'CSR Partnership'),
        ('event', 'Event'),
        ('emergency', 'Emergency Appeal'),
        ('recurring', 'Recurring Giving'),
    ]

    name = models.CharField(max_length=200)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPE_CHOICES, default='general')
    description = models.TextField(blank=True)
    goal_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    owner = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='campaigns'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    @property
    def total_raised(self):
        from finance.models import Payment
        return Payment.objects.filter(
            donation__pledge__campaign=self, status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0


class Pledge(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='pledges')
    campaign = models.ForeignKey(
        Campaign, null=True, blank=True, on_delete=models.SET_NULL, related_name='pledges'
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pledge_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='pledges_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pledge_date']

    def __str__(self):
        return f"{self.donor} – PKR {self.amount} ({self.status})"

    @property
    def amount_paid(self):
        from finance.models import Payment
        return Payment.objects.filter(
            donation__pledge=self, status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def amount_outstanding(self):
        return self.amount - self.amount_paid


class Donation(models.Model):
    pledge = models.ForeignKey(
        Pledge, null=True, blank=True, on_delete=models.SET_NULL, related_name='donations'
    )
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    campaign = models.ForeignKey(
        Campaign, null=True, blank=True, on_delete=models.SET_NULL, related_name='donations'
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    donation_date = models.DateField()
    purpose = models.CharField(max_length=300, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-donation_date']

    def __str__(self):
        return f"{self.donor} – PKR {self.amount} on {self.donation_date}"


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    campaign = models.ForeignKey(
        Campaign, null=True, blank=True, on_delete=models.SET_NULL, related_name='events'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    target_attendees = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='event_participations')
    attended = models.BooleanField(default=False)
    notes = models.CharField(max_length=300, blank=True)

    class Meta:
        unique_together = ('event', 'donor')

    def __str__(self):
        return f"{self.donor} at {self.event}"

