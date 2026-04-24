from django.test import TestCase

from .models import User


class UserModelTests(TestCase):
    def test_user_str_returns_username(self):
        user = User.objects.create(
            username='alice',
            email='alice@example.com',
            password='secret',
            account_number='A0001',
        )
        self.assertEqual(str(user), 'alice')
