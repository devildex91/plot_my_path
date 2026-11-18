from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from destinations.models import Country, Destination

from .models import SavedDestination, TravelPreference

User = get_user_model()


# Helpers


def make_destination(name="Paris", slug="paris"):
    country, _ = Country.objects.get_or_create(
        name="France",
        defaults={"code": "FRA", "continent": "Europe"},
    )
    return Destination.objects.create(
        country=country,
        name=name,
        slug=slug,
        description="A place.",
        latitude=Decimal("48.856600"),
        longitude=Decimal("2.352200"),
        average_cost_per_day=Decimal("150.00"),
    )


# Model tests


class TravelPreferenceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.preference = TravelPreference.objects.create(
            user=cls.user,
            travel_style="adventure",
        )

    def test_preferences_have_expected_defaults(self):
        self.assertEqual(str(self.preference), "Preferences for alice")

        for field in (
            "walking_preference",
            "culture",
            "food",
            "nature",
            "history",
            "nightlife",
            "family_friendly",
            "solo_travel",
        ):
            with self.subTest(field=field):
                self.assertFalse(getattr(self.preference, field))

    def test_invalid_travel_style_is_rejected(self):
        preference = TravelPreference(
            user=self.user,
            travel_style="not-a-valid-style",
        )
        with self.assertRaises(ValidationError):
            preference.full_clean()

    def test_deleting_user_deletes_preferences(self):
        self.user.delete()
        self.assertFalse(TravelPreference.objects.exists())


class SavedDestinationModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.other_user = User.objects.create_user(username="bob", password="pass12345")
        cls.paris = make_destination()
        cls.saved = SavedDestination.objects.create(
            user=cls.user,
            destination=cls.paris,
        )

    def test_saved_destination_string(self):
        self.assertEqual(str(self.saved), "alice saved Paris")
        self.assertIsNotNone(self.saved.created_at)

    def test_user_cannot_save_same_destination_twice(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            SavedDestination.objects.create(
                user=self.user,
                destination=self.paris,
            )

    def test_different_users_can_save_same_destination(self):
        SavedDestination.objects.create(
            user=self.other_user,
            destination=self.paris,
        )
        self.assertEqual(self.paris.saved_by_users.count(), 2)

    def test_deleting_user_or_destination_removes_saved_record(self):
        self.user.delete()
        self.assertEqual(SavedDestination.objects.count(), 0)

        another_user = User.objects.create_user(
            username="charlie", password="pass12345"
        )
        another_destination = make_destination("Rome", "rome")
        SavedDestination.objects.create(
            user=another_user,
            destination=another_destination,
        )

        another_destination.delete()
        self.assertFalse(SavedDestination.objects.exists())


# Shared view test setup


class LoggedInTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.other_user = User.objects.create_user(username="bob", password="pass12345")
        cls.paris = make_destination()
        cls.rome = make_destination("Rome", "rome")

    def setUp(self):
        self.client.force_login(self.user)

    def assert_login_redirect(self, response, url):
        self.assertRedirects(
            response,
            f"{settings.LOGIN_URL}?next={url}",
            fetch_redirect_response=False,
        )


# View tests


class ProfilePageViewTests(LoggedInTestCase):
    def test_login_is_required(self):
        url = reverse("profile")
        self.client.logout()
        self.assert_login_redirect(self.client.get(url), url)

    def test_logged_in_user_can_view_profile(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile_page.html")
        self.assertContains(response, self.user.username)


class FavouriteDestinationsViewTests(LoggedInTestCase):
    def test_login_is_required(self):
        url = reverse("favourite_destinations")
        self.client.logout()
        self.assert_login_redirect(self.client.get(url), url)

    def test_user_only_sees_their_own_saved_destinations(self):
        mine = SavedDestination.objects.create(
            user=self.user,
            destination=self.paris,
        )
        SavedDestination.objects.create(
            user=self.other_user,
            destination=self.rome,
        )

        response = self.client.get(reverse("favourite_destinations"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/favourite_destinations.html")
        self.assertEqual(
            list(response.context["saved_destinations"]),
            [mine],
        )
        self.assertContains(response, "Paris")
        self.assertNotContains(response, "Rome")


class ToggleDestinationFavouriteViewTests(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            "toggle_destination_favourite",
            args=[self.paris.id],
        )

    def test_login_is_required(self):
        self.client.logout()
        self.assert_login_redirect(self.client.post(self.url), self.url)
        self.assertFalse(SavedDestination.objects.exists())

    def test_post_toggles_favourite_on_and_off(self):
        added = self.client.post(self.url)

        self.assertEqual(added.status_code, 200)
        self.assertEqual(added.json(), {"is_favourite": True})
        self.assertTrue(
            SavedDestination.objects.filter(
                user=self.user,
                destination=self.paris,
            ).exists()
        )

        removed = self.client.post(self.url)

        self.assertEqual(removed.status_code, 200)
        self.assertEqual(removed.json(), {"is_favourite": False})
        self.assertFalse(
            SavedDestination.objects.filter(
                user=self.user,
                destination=self.paris,
            ).exists()
        )

    def test_get_is_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_unknown_destination_returns_404(self):
        url = reverse("toggle_destination_favourite", args=[99999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_toggling_does_not_change_another_users_favourite(self):
        SavedDestination.objects.create(
            user=self.other_user,
            destination=self.paris,
        )

        self.client.post(self.url)

        self.assertTrue(
            SavedDestination.objects.filter(
                user=self.other_user,
                destination=self.paris,
            ).exists()
        )
