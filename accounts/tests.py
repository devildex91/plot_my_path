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
        cls.user = User.objects.create_user(
            username="alice", password="pass12345"
        )
        cls.preference = TravelPreference.objects.create(
            user=cls.user,
            travel_style="adventure",
        )

    def test_preferences_have_expected_defaults(self):
        self.assertEqual(str(self.preference), "Preferences for alice")

        for field in (
            "walking_preference", "culture", "food", "nature",
            "history", "nightlife", "family_friendly", "solo_travel",
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
        cls.user = User.objects.create_user(
            username="alice", password="pass12345"
        )
        cls.other_user = User.objects.create_user(
            username="bob", password="pass12345"
        )
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
