import datetime
import json
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError, transaction
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from accounts.models import SavedDestination

from .models import Attraction, Country, Destination


User = get_user_model()


# Helpers


def make_country(name="France", code="FRA", continent="Europe"):
    return Country.objects.create(name=name, code=code, continent=continent)


def make_destination(country, name="Paris", slug="paris"):
    return Destination.objects.create(
        country=country,
        name=name,
        slug=slug,
        description="A place.",
        latitude=Decimal("48.856600"),
        longitude=Decimal("2.352200"),
        average_cost_per_day=Decimal("150.00"),
    )


def make_attraction(destination, name="Louvre", slug="louvre", **overrides):
    data = {
        "destination": destination,
        "name": name,
        "slug": slug,
        "description": "A place of interest.",
        "category": "museum",
        "latitude": Decimal("48.860600"),
        "longitude": Decimal("2.337600"),
        "average_visit_minutes": 120,
        "entry_cost": Decimal("17.00"),
        "opening_time": datetime.time(9, 0),
        "closing_time": datetime.time(18, 0),
    }
    data.update(overrides)
    return Attraction.objects.create(**data)


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.client.force_login(self.user)


# Model Tests


class CountryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = make_country()

    def test_str(self):
        self.assertEqual(str(self.country), "France")

    def test_natural_key(self):
        self.assertEqual(self.country.natural_key(), ("France",))

    def test_get_by_natural_key(self):
        found = Country.objects.get_by_natural_key("France")
        self.assertEqual(found, self.country)

    def test_get_by_natural_key_missing_raises(self):
        with self.assertRaises(Country.DoesNotExist):
            Country.objects.get_by_natural_key("Atlantis")


class DestinationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = make_country()
        cls.destination = make_destination(cls.country)

    def test_str(self):
        self.assertEqual(str(self.destination), "Paris")

    def test_natural_key_uses_slug(self):
        self.assertEqual(self.destination.natural_key(), ("paris",))

    def test_get_by_natural_key(self):
        found = Destination.objects.get_by_natural_key("paris")
        self.assertEqual(found, self.destination)

    def test_slug_must_be_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            make_destination(self.country, name="Paris 2", slug="paris")

    @override_settings(CLOUDINARY_CLOUD_NAME="testcloud")
    def test_get_image_url_uses_cloud_name_and_slug(self):
        self.assertEqual(
            self.destination.get_image_url,
            "https://res.cloudinary.com/testcloud/image/upload/v1/paris",
        )

    def test_related_name_on_country(self):
        self.assertIn(self.destination, self.country.destinations.all())

    def test_deleting_country_deletes_destinations(self):
        self.country.delete()
        self.assertFalse(Destination.objects.exists())


class AttractionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = make_country()
        cls.paris = make_destination(cls.country)
        cls.rome = make_destination(cls.country, name="Rome", slug="rome")
        cls.attraction = make_attraction(cls.paris, "Louvre", "louvre")

    def test_str(self):
        self.assertEqual(str(self.attraction), "Louvre")

    def test_rating_is_optional(self):
        self.assertIsNone(self.attraction.rating)
        self.attraction.full_clean()  # Blank ratings are valid.

    def test_same_slug_not_allowed_within_one_destination(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            make_attraction(self.paris, "Louvre Copy", "louvre")

    def test_same_slug_allowed_in_different_destinations(self):
        other = make_attraction(self.rome, "Louvre Rome", "louvre")
        self.assertEqual(other.slug, self.attraction.slug)

    @override_settings(CLOUDINARY_CLOUD_NAME="testcloud")
    def test_get_image_url(self):
        self.assertEqual(
            self.attraction.get_image_url,
            "https://res.cloudinary.com/testcloud/image/upload/v1/louvre",
        )

    def test_related_name_on_destination(self):
        self.assertIn(self.attraction, self.paris.attractions.all())

    def test_deleting_destination_deletes_attractions(self):
        self.paris.delete()
        self.assertFalse(Attraction.objects.exists())