from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Address, Letting


class AddressModelTest(TestCase):
    """Tests for the Address model."""

    def setUp(self):
        """Set up test data."""
        self.valid_address_data = {
            "number": 123,
            "street": "Main Street",
            "city": "Anytown",
            "state": "CA",
            "zip_code": 12345,
            "country_iso_code": "USA",
        }

    def test_create_valid_address(self):
        """Test creating an address with valid data."""
        address = Address.objects.create(**self.valid_address_data)
        self.assertEqual(address.number, 123)
        self.assertEqual(address.street, "Main Street")
        self.assertEqual(address.city, "Anytown")
        self.assertEqual(address.state, "CA")
        self.assertEqual(address.zip_code, 12345)
        self.assertEqual(address.country_iso_code, "USA")

    def test_address_number_max_validator(self):
        """Test that address number cannot exceed 9999."""
        self.valid_address_data["number"] = 10000
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_address_creation_and_retrieval(self):
        """Test that an address can be created and retrieved."""
        address = Address.objects.create(**self.valid_address_data)
        retrieved = Address.objects.get(id=address.id)
        self.assertEqual(retrieved.number, self.valid_address_data["number"])
        self.assertEqual(retrieved.street, self.valid_address_data["street"])

    def test_state_length_validation(self):
        """Test that state must be exactly 2 characters."""
        self.valid_address_data["state"] = "C"
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()

        self.valid_address_data["state"] = "CAL"
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_country_iso_code_length_validation(self):
        """Test that country_iso_code must be exactly 3 characters."""
        self.valid_address_data["country_iso_code"] = "US"
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()

        self.valid_address_data["country_iso_code"] = "USAA"
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_zip_code_max_validator(self):
        """Test that zip_code cannot exceed 99999."""
        self.valid_address_data["zip_code"] = 100000
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_street_max_length(self):
        """Test that street cannot exceed 64 characters."""
        self.valid_address_data["street"] = "a" * 65
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_city_max_length(self):
        """Test that city cannot exceed 64 characters."""
        self.valid_address_data["city"] = "a" * 65
        address = Address(**self.valid_address_data)
        with self.assertRaises(ValidationError):
            address.full_clean()


class LettingModelTest(TestCase):
    """Tests for the Letting model."""

    def setUp(self):
        """Set up test data."""
        self.address = Address.objects.create(
            number=123,
            street="Main Street",
            city="Anytown",
            state="CA",
            zip_code=12345,
            country_iso_code="USA",
        )

    def test_create_valid_letting(self):
        """Test creating a letting with valid data."""
        letting = Letting.objects.create(
            title="Beautiful Apartment", address=self.address
        )
        self.assertEqual(letting.title, "Beautiful Apartment")
        self.assertEqual(letting.address, self.address)

    def test_title_max_length(self):
        """Test that title cannot exceed 256 characters."""
        long_title = "a" * 257
        letting = Letting(title=long_title, address=self.address)
        with self.assertRaises(ValidationError):
            letting.full_clean()

    def test_address_one_to_one_constraint(self):
        """Test that address can only be assigned to one letting (OneToOne)."""
        Letting.objects.create(title="First Apartment", address=self.address)
        with self.assertRaises(IntegrityError):
            Letting.objects.create(title="Second Apartment", address=self.address)

    def test_cascade_delete(self):
        """Test that deleting address deletes associated letting."""
        letting = Letting.objects.create(title="Test Apartment", address=self.address)

        self.assertTrue(Letting.objects.filter(id=letting.id).exists())

        self.address.delete()

        self.assertFalse(Letting.objects.filter(id=letting.id).exists())


class LettingsViewsTest(TestCase):
    """Tests for lettings views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

        self.address1 = Address.objects.create(
            number=123,
            street="Main Street",
            city="Anytown",
            state="CA",
            zip_code=12345,
            country_iso_code="USA",
        )

        self.address2 = Address.objects.create(
            number=456,
            street="Oak Avenue",
            city="Somewhere",
            state="NY",
            zip_code=54321,
            country_iso_code="USA",
        )

        self.letting1 = Letting.objects.create(
            title="Beautiful Apartment", address=self.address1
        )

        self.letting2 = Letting.objects.create(
            title="Cozy House", address=self.address2
        )

    def test_index_view_status_code(self):
        """Test that index view returns 200."""
        url = reverse("lettings:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        """Test that index view uses correct template."""
        url = reverse("lettings:index")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "lettings/index.html")

    def test_index_view_context(self):
        """Test that index view contains lettings in context."""
        url = reverse("lettings:index")
        response = self.client.get(url)

        self.assertIn("lettings_list", response.context)
        lettings_list = response.context["lettings_list"]
        self.assertEqual(len(lettings_list), 2)
        self.assertIn(self.letting1, lettings_list)
        self.assertIn(self.letting2, lettings_list)

    def test_index_view_content(self):
        """Test that index view contains letting titles."""
        url = reverse("lettings:index")
        response = self.client.get(url)

        self.assertContains(response, "Beautiful Apartment")
        self.assertContains(response, "Cozy House")

    def test_letting_detail_view_status_code(self):
        """Test that letting detail view returns 200."""
        url = reverse("lettings:letting", args=[self.letting1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_letting_detail_view_template(self):
        """Test that letting detail view uses correct template."""
        url = reverse("lettings:letting", args=[self.letting1.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "lettings/letting.html")

    def test_letting_detail_view_context(self):
        """Test that letting detail view contains correct context."""
        url = reverse("lettings:letting", args=[self.letting1.id])
        response = self.client.get(url)

        self.assertIn("title", response.context)
        self.assertIn("address", response.context)
        self.assertEqual(response.context["title"], "Beautiful Apartment")
        self.assertEqual(response.context["address"], self.address1)

    def test_letting_detail_view_content(self):
        """Test that letting detail view contains correct content."""
        url = reverse("lettings:letting", args=[self.letting1.id])
        response = self.client.get(url)

        self.assertContains(response, "Beautiful Apartment")
        self.assertContains(response, "123")
        self.assertContains(response, "Main Street")
        self.assertContains(response, "Anytown")

    def test_letting_detail_view_404(self):
        """Test that letting detail view returns 404 for non-existent letting."""
        url = reverse("lettings:letting", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class LettingsURLsTest(TestCase):
    """Tests for lettings URLs."""

    def setUp(self):
        """Set up test data."""
        address = Address.objects.create(
            number=123,
            street="Main Street",
            city="Anytown",
            state="CA",
            zip_code=12345,
            country_iso_code="USA",
        )

        self.letting = Letting.objects.create(title="Test Apartment", address=address)

    def test_index_url_resolves(self):
        """Test that index URL resolves correctly."""
        url = reverse("lettings:index")
        self.assertEqual(url, "/lettings/")

    def test_letting_detail_url_resolves(self):
        """Test that letting detail URL resolves correctly."""
        url = reverse("lettings:letting", args=[self.letting.id])
        self.assertEqual(url, f"/lettings/{self.letting.id}/")

    def test_index_url_accessible(self):
        """Test that index URL is accessible."""
        response = self.client.get("/lettings/")
        self.assertEqual(response.status_code, 200)

    def test_letting_detail_url_accessible(self):
        """Test that letting detail URL is accessible."""
        response = self.client.get(f"/lettings/{self.letting.id}/")
        self.assertEqual(response.status_code, 200)
