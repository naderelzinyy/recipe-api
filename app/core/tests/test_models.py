"""
Django models test
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTester(TestCase):
    """A tester class contains models tests."""
    def test_user_creation_with_email(self) -> None:
        """Test user creation with email."""
        email = "test@example.com"
        password = "ExamplePassword"

        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_normalization(self) -> None:
        """Test email normalization."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password="sample123")
            self.assertEqual(user.email, expected)
