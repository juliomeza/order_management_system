from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.orders.models import Order, Project

User = get_user_model()

class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass")
        self.project = Project.objects.create(name="Test Project")

        # Obtener token de autenticación
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Datos de prueba
        self.valid_payload = {
            "lookup_code_order": "TEST123",
            "project": self.project.id,
            "status": 1,
            "order_type": 1,
            "order_class": 1,
            "warehouse": 1,
            "contact": 1,
            "shipping_address": 1,
            "billing_address": 1,
            "carrier": None,
            "service_type": None,
            "expected_delivery_date": "2025-02-05T14:15:51Z",
            "notes": "",
            "lines": [
                {"material": 1, "quantity": "2.00", "license_plate": None}
            ]
        }

    def test_create_order_success(self):
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_unauthorized(self):
        self.client.credentials()  # Remueve la autenticación
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_invalid_project(self):
        self.valid_payload["project"] = 999  # Proyecto no válido
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
