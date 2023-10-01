"""
Recipe api tests
"""
from django.test import TestCase
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Recipe
from rest_framework import status
from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse("recipe:recipe-list")


def create_recipe(user, **kwargs):
    """Creates a recipe."""
    recipe_content = {
        "title": "Test recipe title",
        "time_minutes": 10,
        "price": Decimal("20.10"),
        "description": "Testing recipe",
        "link": "http://example.com/recipe.pdf"
    }
    recipe_content.update(**kwargs)
    return Recipe.objects.create(user=user, **recipe_content)


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated requests."""
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        """Test the authentication is required."""
        response = self.client.get(RECIPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated requests."""
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "tester@example.com",
            "pass123",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self) -> None:
        """Test recipes list retrieving."""
        create_recipe(self.user)
        create_recipe(self.user, title="Second test recipe")

        response = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_authenticated_user_recipe(self) -> None:
        """Test for retrieving only the authenticated user's recipes."""
        new_user = get_user_model().objects.create_user(
            "new_user@example.com",
            "pass123"
        )
        create_recipe(user=new_user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
