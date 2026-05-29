from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseTestCase(TestCase):
    def create_user(self, **kwargs):
        defaults = {
            "username": "testuser",
            "password": "pass123",
        }
        defaults.update(kwargs)
        user = User.objects.create_user(**defaults)
        return user


class WishListIndexViewTests(BaseTestCase):
    def test_no_wishlist(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(reverse("wishes:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No wishlists available.")
        self.assertQuerySetEqual(
            response.context["user_wishlists"], [])

    def test_redirect_if_not_logged_in(self):
        """
        Unauthenticated users should ALWAYS redirect to the login page
        """
        response = self.client.get(reverse("wishes:dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
