from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Profile


class ProfileModelTest(TestCase):
    """Tests for the Profile model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="test2@example.com", password="testpass123"
        )

    def test_create_profile_with_favorite_city(self):
        """Test creating a profile with favorite city."""
        profile = Profile.objects.create(user=self.user, favorite_city="Paris")
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.favorite_city, "Paris")

    def test_create_profile_without_favorite_city(self):
        """Test creating a profile without favorite city (blank=True)."""
        profile = Profile.objects.create(user=self.user, favorite_city="")
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.favorite_city, "")

    def test_profile_str_method(self):
        """Test the string representation of Profile returns username."""
        profile = Profile.objects.create(user=self.user, favorite_city="London")
        self.assertEqual(str(profile), "testuser")

    def test_favorite_city_max_length(self):
        """Test that favorite_city cannot exceed 64 characters."""
        long_city = "a" * 65
        profile = Profile(user=self.user, favorite_city=long_city)
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_favorite_city_can_be_blank(self):
        """Test that favorite_city can be blank."""
        profile = Profile(user=self.user, favorite_city="")
        try:
            profile.full_clean()
        except ValidationError:
            self.fail("Profile with blank favorite_city should be valid")

    def test_one_to_one_relationship(self):
        """Test that each user can only have one profile."""
        Profile.objects.create(user=self.user, favorite_city="Paris")
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=self.user, favorite_city="Los Angeles")

    def test_cascade_delete(self):
        """Test that deleting user deletes associated profile."""
        profile = Profile.objects.create(user=self.user, favorite_city="Tokyo")

        self.assertTrue(Profile.objects.filter(id=profile.id).exists())

        self.user.delete()

        self.assertFalse(Profile.objects.filter(id=profile.id).exists())

    def test_profile_user_relationship(self):
        """Test the relationship between Profile and User."""
        profile = Profile.objects.create(user=self.user, favorite_city="Berlin")

        self.assertEqual(profile.user.username, "testuser")
        self.assertEqual(profile.user.email, "test@example.com")

    def test_multiple_profiles_different_users(self):
        """Test that different users can have their own profiles."""
        profile1 = Profile.objects.create(user=self.user, favorite_city="Madrid")

        profile2 = Profile.objects.create(user=self.user2, favorite_city="Rome")

        self.assertEqual(profile1.user, self.user)
        self.assertEqual(profile2.user, self.user2)
        self.assertEqual(Profile.objects.count(), 2)


class ProfilesViewsTest(TestCase):
    """Tests for profiles views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )

        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )

        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="testpass123"
        )

        self.profile1 = Profile.objects.create(user=self.user1, favorite_city="Paris")

        self.profile2 = Profile.objects.create(user=self.user2, favorite_city="London")

        self.profile3 = Profile.objects.create(user=self.user3, favorite_city="")

    def test_index_view_status_code(self):
        """Test that index view returns 200."""
        url = reverse("profiles:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        """Test that index view uses correct template."""
        url = reverse("profiles:index")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "profiles/index.html")

    def test_index_view_context(self):
        """Test that index view contains profiles in context."""
        url = reverse("profiles:index")
        response = self.client.get(url)

        self.assertIn("profiles_list", response.context)
        profiles_list = response.context["profiles_list"]
        self.assertEqual(len(profiles_list), 3)
        self.assertIn(self.profile1, profiles_list)
        self.assertIn(self.profile2, profiles_list)
        self.assertIn(self.profile3, profiles_list)

    def test_index_view_content(self):
        """Test that index view contains usernames."""
        url = reverse("profiles:index")
        response = self.client.get(url)

        self.assertContains(response, "user1")
        self.assertContains(response, "user2")
        self.assertContains(response, "user3")

    def test_profile_detail_view_status_code(self):
        """Test that profile detail view returns 200."""
        url = reverse("profiles:profile", args=[self.user1.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_view_template(self):
        """Test that profile detail view uses correct template."""
        url = reverse("profiles:profile", args=[self.user1.username])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "profiles/profile.html")

    def test_profile_detail_view_context(self):
        """Test that profile detail view contains correct context."""
        url = reverse("profiles:profile", args=[self.user1.username])
        response = self.client.get(url)

        self.assertIn("profile", response.context)
        profile = response.context["profile"]
        self.assertEqual(profile, self.profile1)
        self.assertEqual(profile.user.username, "user1")
        self.assertEqual(profile.favorite_city, "Paris")

    def test_profile_detail_view_content_with_favorite_city(self):
        """Test that profile detail view contains correct content with favorite city."""
        url = reverse("profiles:profile", args=[self.user1.username])
        response = self.client.get(url)

        self.assertContains(response, "user1")
        self.assertContains(response, "Paris")

    def test_profile_detail_view_content_without_favorite_city(self):
        """Test that profile detail view works with empty favorite city."""
        url = reverse("profiles:profile", args=[self.user3.username])
        response = self.client.get(url)

        self.assertContains(response, "user3")
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_view_404_nonexistent_user(self):
        """Test that profile detail view returns 404 for non-existent user."""
        url = reverse("profiles:profile", args=["nonexistentuser"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_profile_detail_view_404_user_without_profile(self):
        """Test that profile detail view returns 404 for user without profile."""
        User.objects.create_user(
            username="noprofile", email="noprofile@example.com", password="testpass123"
        )

        url = reverse("profiles:profile", args=["noprofile"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_index_view_empty_profiles_list(self):
        """Test index view when no profiles exist."""
        Profile.objects.all().delete()

        url = reverse("profiles:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("profiles_list", response.context)
        profiles_list = response.context["profiles_list"]
        self.assertEqual(len(profiles_list), 0)


class ProfilesURLsTest(TestCase):
    """Tests for profiles URLs."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.profile = Profile.objects.create(user=self.user, favorite_city="Tokyo")

    def test_index_url_resolves(self):
        """Test that index URL resolves correctly."""
        url = reverse("profiles:index")
        self.assertEqual(url, "/profiles/")

    def test_profile_detail_url_resolves(self):
        """Test that profile detail URL resolves correctly."""
        url = reverse("profiles:profile", args=[self.user.username])
        self.assertEqual(url, f"/profiles/{self.user.username}/")

    def test_index_url_accessible(self):
        """Test that index URL is accessible."""
        response = self.client.get("/profiles/")
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_url_accessible(self):
        """Test that profile detail URL is accessible."""
        response = self.client.get(f"/profiles/{self.user.username}/")
        self.assertEqual(response.status_code, 200)

    def test_profile_url_with_special_characters(self):
        """Test profile URL with username containing allowed special characters."""
        special_user = User.objects.create_user(
            username="user_123", email="special@example.com", password="testpass123"
        )

        Profile.objects.create(user=special_user, favorite_city="NYC")

        url = reverse("profiles:profile", args=["user_123"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProfileIntegrationTest(TestCase):
    """Integration tests for profiles functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

        self.user = User.objects.create_user(
            username="integrationuser",
            email="integration@example.com",
            password="testpass123",
        )

        self.profile = Profile.objects.create(user=self.user, favorite_city="Amsterdam")

    def test_navigation_from_index_to_detail(self):
        """Test navigation from profiles index to profile detail."""
        index_response = self.client.get(reverse("profiles:index"))
        self.assertEqual(index_response.status_code, 200)

        detail_url = reverse("profiles:profile", args=[self.user.username])
        self.assertContains(index_response, self.user.username)

        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Amsterdam")

    def test_profile_creation_and_display(self):
        """Test complete flow of profile creation and display."""
        new_user = User.objects.create_user(
            username="newflowuser", email="newflow@example.com", password="testpass123"
        )

        Profile.objects.create(user=new_user, favorite_city="Barcelona")

        index_response = self.client.get(reverse("profiles:index"))
        self.assertContains(index_response, "newflowuser")

        detail_response = self.client.get(
            reverse("profiles:profile", args=["newflowuser"])
        )
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Barcelona")
