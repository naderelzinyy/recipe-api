"""
Tests for user api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")


def create_user(**kwargs):
    """Creates a new user."""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserTests(TestCase):
    """Contains all the tests that don't require authentication."""
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self) -> None:
        """Test success of creating a user."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Tester test"
        }
        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", result.data)

    def test_user_with_email_exist_error(self) -> None:
        """Tests the error of email existence."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Tester test"
        }
        create_user(**payload)
        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self) -> None:
        """Tests if the password is shorter than 5 characters."""
        payload = {
            "email": "test@example.com",
            "password": "123",
            "name": "Tester test"
        }

        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        is_user_exist = get_user_model().objects.filter(
            email=payload["email"],
        ).exists()
        self.assertFalse(is_user_exist)
