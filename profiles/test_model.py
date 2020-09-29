from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestUserProfile(TestCase):
    """ Testing class for User profile """

    def test_create_or_update_user_profile(self):
        user_data = {
            'username': 'username',
            'password': 'password',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email',
        }
        user = User.objects.create_user(**user_data)
        self.assertTrue(UserProfile.objects.get(user=user.id))

