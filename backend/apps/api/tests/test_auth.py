from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.core.models import Status
from apps.customers.models import Project, Customer
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        # Create status
        self.status = Status.objects.create(
            name="Active",
            code="ACTIVE",
            status_type="Global",
            is_active=True
        )

        # Create customer and project
        self.customer = Customer.objects.create(
            name="Test Customer",
            lookup_code="CUST001",
            status=self.status
        )

        self.project = Project.objects.create(
            name="Test Project",
            lookup_code="PRJ001",
            orders_prefix="TP",
            customer=self.customer,
            status=self.status
        )

        # Create active user
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com", 
            password="testpass",
            status=self.status,
            project=self.project,
            is_active=True
        )

        # Create inactive user
        self.inactive_user = User.objects.create_user(
            username="inactive",
            email="inactive@example.com",
            password="testpass",
            status=self.status,
            is_active=False
        )

        # Base URL for token endpoints
        self.token_url = "/api/token/"
        self.refresh_url = "/api/token/refresh/"

    def test_obtain_token_success(self):
        """Test successful token obtain with valid credentials"""
        response = self.client.post(self.token_url, {
            "email": "user@example.com",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Verify token contains user_id
        access_token = response.data["access"]
        decoded_token = AccessToken(access_token)
        self.assertEqual(decoded_token["user_id"], self.user.id)

    def test_invalid_credentials(self):
        """Test token obtain with invalid credentials"""
        response = self.client.post(self.token_url, {
            "email": "user@example.com",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_refresh_token_success(self):
        """Test successful token refresh"""
        # First obtain tokens
        response = self.client.post(self.token_url, {
            "email": "user@example.com",
            "password": "testpass"
        })
        refresh_token = response.data["refresh"]

        # Then refresh
        response = self.client.post(self.refresh_url, {
            "refresh": refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_invalid_refresh_token(self):
        """Test refresh token with invalid token"""
        response = self.client.post(self.refresh_url, {
            "refresh": "invalid_token"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_credentials(self):
        """Test token obtain with missing credentials"""
        # Test missing password
        response = self.client.post(self.token_url, {
            "email": "user@example.com"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test missing email
        response = self.client.post(self.token_url, {
            "password": "testpass"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user(self):
        """Test token obtain with inactive user"""
        response = self.client.post(self.token_url, {
            "email": "inactive@example.com",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_malformed_token_refresh(self):
        """Test refresh token endpoint with malformed token"""
        response = self.client.post(self.refresh_url, {
            "refresh": "malformed.token.here"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_refresh_token(self):
        """Test refresh token endpoint with missing token"""
        response = self.client.post(self.refresh_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)