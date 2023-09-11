"""
User api views
"""

from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """User creation view."""
    serializer_class = UserSerializer
