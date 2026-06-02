from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from donors.models import Donor
from campaigns.models import Campaign, Pledge, Donation
from finance.models import Payment


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_donors = Donor.objects.filter(is_active=True).count()
        total_campaigns = Campaign.objects.filter(status='active').count()

        total_raised = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0

        outstanding_pledges = Pledge.objects.filter(
            status__in=['pending', 'partial']
        ).aggregate(total=Sum('amount'))['total'] or 0

        recent_donations = Donation.objects.select_related('donor', 'campaign').order_by(
            '-donation_date'
        )[:10].values('id', 'donor__id', 'amount', 'donation_date', 'campaign__name')

        return Response({
            'total_active_donors': total_donors,
            'total_active_campaigns': total_campaigns,
            'total_raised': total_raised,
            'outstanding_pledges': outstanding_pledges,
            'recent_donations': list(recent_donations),
        })


class CampaignPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campaigns = Campaign.objects.annotate(
            donation_count=Count('donations'),
            total_donated=Sum('donations__payments__amount'),
        ).values(
            'id', 'name', 'campaign_type', 'goal_amount',
            'donation_count', 'total_donated', 'status',
        )
        return Response(list(campaigns))


class DonorRetentionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        year = now.year

        donors_this_year = set(
            Donation.objects.filter(donation_date__year=year)
            .values_list('donor_id', flat=True)
        )
        donors_last_year = set(
            Donation.objects.filter(donation_date__year=year - 1)
            .values_list('donor_id', flat=True)
        )

        retained = len(donors_this_year & donors_last_year)
        new_donors = len(donors_this_year - donors_last_year)
        lapsed = len(donors_last_year - donors_this_year)

        retention_rate = (retained / len(donors_last_year) * 100) if donors_last_year else 0

        return Response({
            'year': year,
            'retained_donors': retained,
            'new_donors': new_donors,
            'lapsed_donors': lapsed,
            'retention_rate': round(retention_rate, 2),
        })


class FinancialReconciliationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        by_mode = Payment.objects.filter(status='completed').values('payment_mode').annotate(
            total=Sum('amount'), count=Count('id')
        )
        by_status = Payment.objects.values('status').annotate(
            total=Sum('amount'), count=Count('id')
        )
        return Response({
            'by_payment_mode': list(by_mode),
            'by_status': list(by_status),
        })

