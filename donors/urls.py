from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DonorViewSet, DonorDocumentViewSet, DonorEngagementViewSet

router = DefaultRouter()
router.register('donors', DonorViewSet)
router.register('donor-documents', DonorDocumentViewSet)
router.register('donor-engagements', DonorEngagementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
