"""
Django models test
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from decimal import Decimal
from core import models


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
            user = get_user_model().objects.create_user(
                email=email,
                password="sample123"
            )
            self.assertEqual(user.email, expected)

    def test_email_is_not_empty(self) -> None:
        """Test the email empty or not."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_super_user(self) -> None:
        """Test the creation of superuser."""
        user = get_user_model().objects.create_superuser(
            email="superuser@example.com", password="test123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self) -> None:
        """Test for recipe creation."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "pass123"
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="First recipe",
            time_minutes=5,
            price=Decimal("20.50"),
            description="A delicious first recipe."
        )
        self.assertEqual(str(recipe), recipe.title)
