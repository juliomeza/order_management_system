from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.logistics.models import Contact, Address
from apps.api.tests.factories import (
    ContactFactory, UserFactory, 
    ProjectFactory, StatusFactory
)

class ContactAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Clear existing data
        Contact.objects.all().delete()
        Address.objects.filter(entity_type='recipient').delete()
        
        # Create base objects
        self.status = StatusFactory()
        self.project = ProjectFactory()
        self.user = UserFactory(project=self.project)
        
        # Setup authentication
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "john.doe@example.com",
            "mobile": "0987654321",
            "title": "Manager",
            "notes": "Test contact",
            "addresses": [
                {
                    "address_line_1": "123 Main St",
                    "address_line_2": "Apt 4B",
                    "city": "Miami",
                    "state": "FL",
                    "postal_code": "33101",
                    "country": "USA",
                    "address_type": "shipping",
                    "notes": "Main office"
                },
                {
                    "address_line_1": "456 Second St",
                    "city": "Miami",
                    "state": "FL",
                    "postal_code": "33102",
                    "country": "USA",
                    "address_type": "billing",
                    "notes": "Billing address"
                }
            ]
        }

    def test_create_contact_success(self):
        """Test creating a contact with multiple addresses"""
        response = self.client.post("/api/contacts/", self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Address.objects.filter(entity_type='recipient').count(), 2)
        
        contact = Contact.objects.first()
        self.assertIn(self.project, contact.projects.all())
        self.assertEqual(contact.addresses.count(), 2)
        self.assertTrue(contact.addresses.filter(address_type="shipping").exists())
        self.assertTrue(contact.addresses.filter(address_type="billing").exists())

    def test_create_contact_without_addresses(self):
        """Test creating a contact without addresses"""
        payload = self.valid_payload.copy()
        payload.pop("addresses")
        response = self.client.post("/api/contacts/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Address.objects.filter(entity_type='recipient').count(), 0)

    def test_create_contact_with_invalid_address(self):
        """Test creating a contact with invalid address data"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload["addresses"][0].pop("city")
        response = self.client.post("/api/contacts/", invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertEqual(Address.objects.filter(entity_type='recipient').count(), 0)
        self.assertIn('addresses', response.data['detail'])

    def test_get_contacts_list(self):
        """Test retrieving contacts list for user's project"""
        # Create contact for user's project
        contact1 = ContactFactory.create(projects=[self.project])
        
        # Create contact for other project
        other_project = ProjectFactory()
        contact2 = ContactFactory.create(projects=[other_project])

        response = self.client.get("/api/contacts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], contact1.first_name)

    def test_get_contacts_unauthenticated(self):
        """Test accessing contacts without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_contact_with_multiple_addresses(self):
        """Test creating a contact with multiple valid addresses"""
        payload = self.valid_payload.copy()
        payload["addresses"].append({
            "address_line_1": "789 Third St",
            "city": "Miami",
            "state": "FL",
            "postal_code": "33103",
            "country": "USA",
            "address_type": "shipping",
            "notes": "Additional shipping address"
        })

        response = self.client.post("/api/contacts/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.first()
        self.assertEqual(contact.addresses.filter(entity_type='recipient').count(), 3)

    def test_create_contact_missing_required_fields(self):
        """Test creating a contact with missing required fields"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload.pop("first_name")
        invalid_payload.pop("phone")

        response = self.client.post("/api/contacts/", invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data["detail"])
        self.assertIn("phone", response.data["detail"])

    def test_create_contact_invalid_email(self):
        """Test creating a contact with invalid email format"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = "invalid-email"
        
        response = self.client.post("/api/contacts/", invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["detail"])

    def test_create_contact_invalid_address_type(self):
        """Test creating a contact with invalid address type"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload["addresses"][0]["address_type"] = "invalid_type"
        
        response = self.client.post("/api/contacts/", invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("addresses", response.data["detail"])