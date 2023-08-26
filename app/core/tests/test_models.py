"""
Django models test
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTester(TestCase):
    """A tester class contains models tests."""
    def test_user_creation_with_email(self):
        """Test user creation with email."""
        email = "test@example.com"
        password = "ExamplePassword"

        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
