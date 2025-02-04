from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APITestCase
from apps.api.tests.factories import UserFactory

class OrderSerializerTest(APITestCase):
    def setUp(self):
        """Set up auth test data"""
        self.user = UserFactory()
        self.inactive_user = UserFactory(is_active=False)

        # Base URL for token endpoints
        self.token_url = "/api/token/"
        self.refresh_url = "/api/token/refresh/"
        self.logout_url = "/api/token/logout/"

    def test_obtain_token_success(self):
        """Test successful token obtain with valid credentials"""
        response = self.client.post(self.token_url, {
            "email": self.user.email,
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
            "email": self.user.email,
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_refresh_token_success(self):
        """Test successful token refresh"""
        # First obtain tokens
        response = self.client.post(self.token_url, {
            "email": self.user.email,
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
            "email": self.user.email,
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
            "email": self.inactive_user.email,
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

    def test_logout_success(self):
        """Test successful logout by blacklisting refresh token"""
        # First obtain tokens
        auth_response = self.client.post(self.token_url, {
            "email": self.user.email,
            "password": "testpass"
        })
        refresh_token = auth_response.data["refresh"]

        # Then logout
        response = self.client.post(self.logout_url, {
            "refresh": refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify token can't be used anymore
        refresh_response = self.client.post(self.refresh_url, {
            "refresh": refresh_token
        })
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_without_token(self):
        """Test logout attempt without providing refresh token"""
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_with_invalid_token(self):
        """Test logout attempt with invalid refresh token"""
        response = self.client.post(self.logout_url, {
            "refresh": "invalid_token"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_access_token(self):
        """Test using an expired access token"""
        # First obtain tokens with normal lifetime
        response = self.client.post(self.token_url, {
            "email": self.user.email,
            "password": "testpass"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        # Override the token's exp claim to make it expired
        token = AccessToken(access_token)
        exp_timestamp = timezone.now() - timedelta(days=1)  # Token expired yesterday
        token.payload['exp'] = datetime.timestamp(exp_timestamp)
        expired_token = str(token)

        # Try to use the expired token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        response = self.client.get("/api/contacts/")  # Use any protected endpoint
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Given token not valid for any token type", str(response.data["detail"]))

    def test_refresh_token_after_logout(self):
        """Test attempting to refresh token after logout"""
        # First obtain tokens
        auth_response = self.client.post(self.token_url, {
            "email": self.user.email,
            "password": "testpass"
        })
        refresh_token = auth_response.data["refresh"]

        # Logout
        self.client.post(self.logout_url, {
            "refresh": refresh_token
        })

        # Try to use the blacklisted refresh token
        response = self.client.post(self.refresh_url, {
            "refresh": refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)