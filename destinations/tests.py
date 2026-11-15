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
from .views import popular_destinations

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


# Models


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


# Views


class DestinationListViewTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.france = make_country("France", "FRA", "Europe")
        cls.spain = make_country("Spain", "ESP", "Europe")
        cls.japan = make_country("Japan", "JPN", "Asia")
        cls.paris = make_destination(cls.france, "Paris", "paris")
        cls.madrid = make_destination(cls.spain, "Madrid", "madrid")
        cls.tokyo = make_destination(cls.japan, "Tokyo", "tokyo")
        cls.url = reverse("destination_lists")

    def test_logged_out_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{settings.LOGIN_URL}?next={self.url}",
            fetch_redirect_response=False,
        )

    def test_default_shows_all_destinations(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "destinations/destination.html")
        self.assertEqual(response.context["selected_continent"], "all")
        self.assertEqual(
            set(response.context["destinations"]),
            {self.paris, self.madrid, self.tokyo},
        )

    def test_continent_filter_returns_only_matching(self):
        response = self.client.get(self.url, {"continent": "Asia"})
        self.assertEqual(list(response.context["destinations"]), [self.tokyo])
        self.assertEqual(response.context["selected_continent"], "Asia")

    def test_continent_filter_is_case_insensitive(self):
        response = self.client.get(self.url, {"continent": "europe"})
        self.assertEqual(
            set(response.context["destinations"]), {self.paris, self.madrid}
        )

    def test_unknown_continent_gives_empty_list(self):
        response = self.client.get(self.url, {"continent": "Atlantis"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["destinations"]), [])

    def test_continents_are_distinct_and_sorted(self):
        response = self.client.get(self.url)
        self.assertEqual(list(response.context["continents"]), ["Asia", "Europe"])


class DestinationDetailViewTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.other = User.objects.create_user(username="bob", password="pass12345")
        cls.country = make_country()
        cls.paris = make_destination(cls.country, "Paris", "paris")
        cls.rome = make_destination(cls.country, "Rome", "rome")
        cls.louvre = make_attraction(cls.paris, "Louvre", "louvre")
        cls.colosseum = make_attraction(cls.rome, "Colosseum", "colosseum")
        cls.url = reverse("details", args=[cls.paris.id])

    def test_logged_out_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{settings.LOGIN_URL}?next={self.url}",
            fetch_redirect_response=False,
        )

    def test_renders_with_correct_destination(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "destinations/destination_detail.html")
        self.assertEqual(response.context["destination"], self.paris)

    def test_nonexistent_destination_returns_404(self):
        response = self.client.get(reverse("details", args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_only_this_destinations_attractions_are_listed(self):
        response = self.client.get(self.url)
        self.assertEqual(list(response.context["attractions"]), [self.louvre])

    def test_is_favourite_false_by_default(self):
        response = self.client.get(self.url)
        self.assertFalse(response.context["is_favourite"])

    def test_is_favourite_true_after_saving(self):
        SavedDestination.objects.create(user=self.user, destination=self.paris)
        response = self.client.get(self.url)
        self.assertTrue(response.context["is_favourite"])

    def test_is_favourite_ignores_other_users_saves(self):
        SavedDestination.objects.create(user=self.other, destination=self.paris)
        response = self.client.get(self.url)
        self.assertFalse(response.context["is_favourite"])


class SearchDestinationsViewTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.country = make_country()
        cls.paris = make_destination(cls.country, "Paris", "paris")
        cls.url = reverse("search_destinations")

    def test_logged_out_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(self.url, {"q": "par"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.LOGIN_URL, response.url)

    def test_missing_query_returns_empty_results(self):
        response = self.client.get(self.url)
        self.assertEqual(response.json(), {"results": []})

    def test_whitespace_query_returns_empty_results(self):
        response = self.client.get(self.url, {"q": "   "})
        self.assertEqual(response.json(), {"results": []})

    def test_partial_case_insensitive_match(self):
        response = self.client.get(self.url, {"q": "PAR"})
        results = response.json()["results"]
        self.assertEqual([r["name"] for r in results], ["Paris"])

    def test_no_match_returns_empty_results(self):
        response = self.client.get(self.url, {"q": "zzz"})
        self.assertEqual(response.json(), {"results": []})

    @override_settings(CLOUDINARY_CLOUD_NAME="testcloud")
    def test_result_shape(self):
        response = self.client.get(self.url, {"q": "paris"})
        self.assertEqual(
            response.json()["results"][0],
            {
                "id": self.paris.id,
                "name": "Paris",
                "slug": "paris",
                "description": "A place.",
                "cost": "150.00",  # Decimal is serialised as a string
                "image_url": "https://res.cloudinary.com/testcloud/image/upload/v1/paris",
            },
        )

    def test_results_capped_at_ten(self):
        for i in range(12):
            make_destination(self.country, f"Town {i}", f"town-{i}")
        response = self.client.get(self.url, {"q": "town"})
        self.assertEqual(len(response.json()["results"]), 10)


class PopularDestinationsViewTests(TestCase):
    """Called directly with RequestFactory because the view has no URL yet."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.country = make_country()
        cls.factory = RequestFactory()

    def _get(self, user):
        request = self.factory.get("/popular/")
        request.user = user
        return popular_destinations(request)

    def test_logged_out_redirects_to_login(self):
        response = self._get(AnonymousUser())
        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.LOGIN_URL, response.url)

    def test_empty_database_returns_empty_results(self):
        response = self._get(self.user)
        self.assertEqual(json.loads(response.content), {"results": []})

    def test_returns_all_when_fewer_than_three(self):
        make_destination(self.country, "Paris", "paris")
        make_destination(self.country, "Lyon", "lyon")
        response = self._get(self.user)
        self.assertEqual(len(json.loads(response.content)["results"]), 2)

    def test_capped_at_three(self):
        for i in range(5):
            make_destination(self.country, f"Town {i}", f"town-{i}")
        response = self._get(self.user)
        self.assertEqual(len(json.loads(response.content)["results"]), 3)
