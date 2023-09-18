"""
Tests for user api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


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

    def test_create_token_for_user(self) -> None:
        """Test for validation token creation."""

        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "testexample123"
        }

        create_user(**user_details)

        payload = {
            "email": user_details.get("email"),
            "password": user_details.get("password")
        }

        response = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_credentials_token_creation(self) -> None:
        """Test for token creation with bad credentials."""
        create_user(email="test@example.com", password="password123")

        payload = {
            "email": "wrongtest@example.com",
            "password": "wrong pass"
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserTests(TestCase):
    """Contains the tests that require authentication."""
    def setUp(self) -> None:
        self.user = create_user(
            email="testexp@example.com",
            password="pass123",
            name="test exp"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_successful_profile_retrieving(self) -> None:
        """Test for success profile retrieve."""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "name": self.user.name,
            "email": self.user.email
        })

    def test_post_not_allowed(self) -> None:
        """Test post functions not allowed for ME_URL"""
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_info(self) -> None:
        """Test for updating user profile data."""
        payload = {
            "name": "new name",
            "password": "newpass123"
        }
        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload.get("name"))
        self.assertTrue(self.user.check_password(payload.get("password")))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
