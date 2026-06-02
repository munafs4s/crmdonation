from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EmailTemplateViewSet, CommunicationLogViewSet, BulkCommunicationViewSet

router = DefaultRouter()
router.register('email-templates', EmailTemplateViewSet)
router.register('communication-logs', CommunicationLogViewSet)
router.register('bulk-communications', BulkCommunicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
