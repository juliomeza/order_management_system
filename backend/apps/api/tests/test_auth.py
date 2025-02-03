from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.core.models import Status

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.status = Status.objects.create(
            name="Active",
            code="ACTIVE",
            status_type="Global",
            is_active=True
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com", 
            password="testpass",
            status=self.status
        )

    def test_obtain_token(self):
        response = self.client.post("/api/token/", {"email": "user@example.com", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_invalid_credentials(self):
        response = self.client.post("/api/token/", {"email": "user@example.com", "password": "wrongpass"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        token = self.client.post("/api/token/", {"email": "user@example.com", "password": "testpass"}).data["refresh"]
        response = self.client.post("/api/token/refresh/", {"refresh": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
