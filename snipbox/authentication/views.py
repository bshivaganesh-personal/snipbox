"""Custom authentication views for SnipBox."""

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extend the default serializer to include user info in response."""

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra user info to the response
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data


class CustomLoginView(TokenObtainPairView):
    """Custom login view returning tokens + user details."""

    serializer_class = CustomTokenObtainPairSerializer