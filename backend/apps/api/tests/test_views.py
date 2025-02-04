from rest_framework import status
from apps.orders.models import Order
from apps.api.tests.test_base import BaseAPITestCase

class OrderAPITestCase(BaseAPITestCase):
    def setUp(self):
        """Set up test data"""
        super().setUp()
        
        # Valid payload for creating orders
        self.valid_payload = {
            "lookup_code_order": "TEST123",
            "lookup_code_shipment": "SHIP123",
            "project": self.project.id,
            "status": self.status_project.id,
            "order_type": self.order_type.id,
            "order_class": self.order_class.id,
            "warehouse": self.warehouse.id,
            "contact": self.contact.id,
            "shipping_address": self.shipping_address.id,
            "billing_address": self.billing_address.id,
            "carrier": None,
            "service_type": None,
            "expected_delivery_date": "2025-02-05T14:15:51Z",
            "notes": "",
            "lines": [
                {
                    "material": self.material.id,
                    "quantity": "2.00",
                    "license_plate": None,
                    "serial_number": None,
                    "lot": "",
                    "vendor_lot": "",
                    "notes": ""
                }
            ]
        }

    def test_get_orders_success(self):
        """Test retrieving orders for authenticated user"""
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_unauthorized(self):
        """Test retrieving orders without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_success(self):
        """Test creating a valid order"""
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().lookup_code_order, "TEST123")

    def test_create_order_unauthorized(self):
        """Test creating order without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_invalid_project(self):
        """Test creating order for invalid project"""
        self.valid_payload["project"] = self.other_project.id
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_insufficient_inventory(self):
        """Test creating order with insufficient inventory"""
        self.valid_payload["lines"][0]["quantity"] = "100.00"  # More than available
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_missing_lines(self):
        """Test creating order without order lines"""
        self.valid_payload["lines"] = []
        response = self.client.post("/api/orders/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)