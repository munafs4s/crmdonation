from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TaskViewSet, ReminderViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('reminders', ReminderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
