from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from gifting.models import Event

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

    def create_event(self, **kwargs):
        defaults = {
            "name": "Christmas",
            "date": "2026-12-25"
        }
        defaults.update(kwargs)
        return Event.objects.create(**defaults)


class WishListIndexViewTests(BaseTestCase):
    def test_no_wishlist(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(reverse("gifting:wishlist_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No wishlists available.")
        self.assertQuerySetEqual(
            response.context["user_wishlists"], [])

    def test_redirect_if_not_logged_in(self):
        """
        Unauthenticated users should ALWAYS redirect to the login page
        """
        response = self.client.get(reverse("gifting:wishlist_list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class EventDetailViewTests(BaseTestCase):
    def setUp(self):
        self.user = self.create_user()
        self.client.force_login(self.user)
        self.event = self.create_event()
        self.event.participants.create(
            user=self.user
        )

    def test_htmx_event_detail_returns_partial(self):

        response = self.client.get(
            reverse("gifting:event_detail", args=[self.event.pk]),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "gifting/partials/events/_event_detail_htmx.html"
        )

    def test_event_detail_returns_dashboard(self):
        response = self.client.get(
            reverse("gifting:event_detail", args=[self.event.pk])
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "gifting/partials/events/_dashboard.html"
        )

    def test_event_detail_includes_event_in_context(self):
        response = self.client.get(
            reverse("gifting:event_detail", args=[self.event.pk])
        )

        self.assertEqual(response.context["object"], self.event)
        self.assertIn(
            self.event,
            response.context["user_events"]
        )
