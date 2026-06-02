from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CampaignViewSet, PledgeViewSet, DonationViewSet, EventViewSet, EventParticipantViewSet

router = DefaultRouter()
router.register('campaigns', CampaignViewSet)
router.register('pledges', PledgeViewSet)
router.register('donations', DonationViewSet)
router.register('events', EventViewSet)
router.register('event-participants', EventParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
