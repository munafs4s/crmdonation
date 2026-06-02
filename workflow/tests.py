from django.test import TestCase
from django.contrib.auth.models import User
from donors.models import Donor
from workflow.models import Task, Reminder
from django.utils import timezone


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='wfuser', password='pass')
        self.donor = Donor.objects.create(email='wf@test.com')

    def test_task_str(self):
        task = Task.objects.create(
            title='Follow up with donor',
            task_type='follow_up',
            assigned_to=self.user,
            donor=self.donor,
        )
        self.assertEqual(str(task), 'Follow up with donor')

    def test_task_default_status(self):
        task = Task.objects.create(title='Test Task')
        self.assertEqual(task.status, 'pending')

    def test_task_default_priority(self):
        task = Task.objects.create(title='Low Priority Task')
        self.assertEqual(task.priority, 'medium')


class ReminderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='remuser', password='pass')
        self.donor = Donor.objects.create(email='rem@test.com')

    def test_reminder_str(self):
        remind_at = timezone.now() + timezone.timedelta(days=1)
        reminder = Reminder.objects.create(
            reminder_type='pledge_due',
            message='Pledge is due',
            remind_at=remind_at,
            donor=self.donor,
            created_by=self.user,
        )
        self.assertIn('pledge_due', str(reminder))

    def test_reminder_default_not_sent(self):
        remind_at = timezone.now() + timezone.timedelta(days=1)
        reminder = Reminder.objects.create(
            reminder_type='custom',
            message='Test reminder',
            remind_at=remind_at,
        )
        self.assertFalse(reminder.sent)

