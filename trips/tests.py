import datetime
import json
from decimal import Decimal
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.models import TravelPreference
from destinations.models import Attraction, Country, Destination
from payments.models import PremiumMembership

from .forms import (
    DestinationWizardForm,
    PreferenceWizardForm,
    ReviewForm,
    TripDetailsWizardForm,
)
from .models import PlannedActivity, Recommendation, Trip, TripDay
from .permissions import can_create_trip, is_premium
from .views import get_destination_weather

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


def make_attraction(destination, name="Louvre", slug="louvre"):
    return Attraction.objects.create(
        destination=destination,
        name=name,
        slug=slug,
        description="A place of interest.",
        category="museum",
        latitude=Decimal("48.860600"),
        longitude=Decimal("2.337600"),
        average_visit_minutes=120,
        entry_cost=Decimal("17.00"),
        opening_time=datetime.time(9, 0),
        closing_time=datetime.time(18, 0),
    )


def make_trip(user, destination, name="Trip"):
    return Trip.objects.create(
        user=user,
        destination=destination,
        name=name,
        start_date=datetime.date(2026, 12, 1),
        end_date=datetime.date(2026, 12, 3),
        budget=Decimal("100.00"),
    )


def make_activity(day, attraction, start, end, order=1):
    return PlannedActivity.objects.create(
        trip_day=day,
        attraction=attraction,
        start_time=start,
        end_time=end,
        order=order,
    )


# Models


class TripTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.destination = make_destination()
        cls.trip = Trip.objects.create(
            user=cls.user,
            destination=cls.destination,
            name="Paris Break",
            start_date=datetime.date(2026, 12, 1),
            end_date=datetime.date(2026, 12, 5),
            budget=Decimal("1000.00"),
        )
        cls.day = TripDay.objects.create(
            trip=cls.trip,
            date=datetime.date(2026, 12, 1),
            day_number=1,
        )
        cls.attraction = make_attraction(cls.destination)
        cls.activity = make_activity(
            cls.day,
            cls.attraction,
            datetime.time(10, 0),
            datetime.time(12, 0),
        )

    def test_model_strings_and_defaults(self):
        self.assertEqual(str(self.trip), "Paris Break")
        self.assertEqual(str(self.day), "Day 1 - Paris Break")
        self.assertEqual(str(self.activity), "Louvre (10:00:00)")
        self.assertEqual(self.activity.status, "scheduled")

    def test_budget_too_large_fails_validation(self):
        trip = Trip(
            user=self.user,
            destination=self.destination,
            name="Too rich",
            start_date=datetime.date(2026, 12, 1),
            end_date=datetime.date(2026, 12, 2),
            budget=Decimal("100000000.00"),
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_deleting_user_deletes_trips(self):
        self.user.delete()
        self.assertFalse(Trip.objects.exists())

    def test_deleting_trip_deletes_days_and_activities(self):
        self.trip.delete()
        self.assertFalse(TripDay.objects.exists())
        self.assertFalse(PlannedActivity.objects.exists())

class RecommendationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="alice",
            password="pass12345",
        )
        country = Country.objects.create(name="France", code="FRA", continent="Europe")
        cls.destination = Destination.objects.create(
            country=country,
            name="Paris",
            slug="paris",
            description="The city of light.",
            latitude=Decimal("48.856600"),
            longitude=Decimal("2.352200"),
            average_cost_per_day=Decimal("150.00"),
        )
        cls.attraction = Attraction.objects.create(
            destination=cls.destination,
            name="Eiffel Tower",
            slug="eiffel-tower",
            description="An iron lattice tower.",
            category="landmark",
            latitude=Decimal("48.858400"),
            longitude=Decimal("2.294500"),
            average_visit_minutes=90,
            entry_cost=Decimal("25.00"),
            opening_time=datetime.time(9, 0),
            closing_time=datetime.time(23, 0),
        )
        cls.trip = Trip.objects.create(
            user=cls.user,
            destination=cls.destination,
            name="Paris Trip",
            start_date=datetime.date(2026, 12, 1),
            end_date=datetime.date(2026, 12, 5),
            budget=Decimal("1000.00"),
        )

    def make_recommendation(self, score):
        return Recommendation.objects.create(
            user=self.user,
            trip=self.trip,
            attraction=self.attraction,
            score=score,
            reason="Matches your interests",
        )

    def test_recommendation_creation(self):
        recommendation = self.make_recommendation(Decimal("85.50"))

        self.assertEqual(recommendation.score, Decimal("85.50"))
        self.assertEqual(recommendation.reason, "Matches your interests")
        self.assertEqual(recommendation.user, self.user)
        self.assertEqual(recommendation.trip, self.trip)
        self.assertEqual(recommendation.attraction, self.attraction)

    def test_string_representation(self):
        recommendation = self.make_recommendation("85.50")

        self.assertEqual(
            str(recommendation),
            "Rec for alice: Eiffel Tower (Score: 85.50)",
        )

    def test_recommendations_are_ordered_by_score(self):
        low = self.make_recommendation("40.00")
        high = self.make_recommendation("90.00")

        recommendations = list(Recommendation.objects.all())

        self.assertEqual(recommendations, [high, low])

    def test_deleting_user_deletes_recommendations(self):
        self.make_recommendation("85.50")

        self.user.delete()

        self.assertFalse(Recommendation.objects.exists())

    def test_deleting_trip_deletes_recommendations(self):
        self.make_recommendation("85.50")

        self.trip.delete()

        self.assertFalse(Recommendation.objects.exists())

    def test_deleting_attraction_deletes_recommendations(self):
        self.make_recommendation("85.50")

        self.attraction.delete()

        self.assertFalse(Recommendation.objects.exists())

# Shared view test setup


class TripsViewTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="pass12345")
        cls.other = User.objects.create_user(username="bob", password="pass12345")
        cls.paris = make_destination()
        cls.rome = make_destination("Rome", "rome")
        cls.louvre = make_attraction(cls.paris)
        cls.colosseum = make_attraction(cls.rome, "Colosseum", "colosseum")
        cls.trip = Trip.objects.create(
            user=cls.user,
            destination=cls.paris,
            name="Paris Break",
            start_date=datetime.date(2026, 12, 1),
            end_date=datetime.date(2026, 12, 5),
            budget=Decimal("1000.00"),
        )
        cls.day = TripDay.objects.create(
            trip=cls.trip,
            date=datetime.date(2026, 12, 1),
            day_number=1,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def assert_login_redirect(self, response, url):
        self.assertRedirects(
            response,
            f"{settings.LOGIN_URL}?next={url}",
            fetch_redirect_response=False,
        )

# Views


class MyTripsViewTests(TripsViewTestBase):
    def setUp(self):
        super().setUp()
        self.url = reverse("my_trips")

    def test_login_is_required(self):
        self.client.logout()
        self.assert_login_redirect(self.client.get(self.url), self.url)

    def test_user_only_sees_their_own_trips(self):
        make_trip(self.other, self.paris, "Bob's trip")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["trips"]), [self.trip])


class DeleteTripViewTests(TripsViewTestBase):
    def setUp(self):
        super().setUp()
        self.url = reverse("delete_trip", args=[self.trip.id])

    def test_post_deletes_trip_and_redirects(self):
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse("my_trips"),
            fetch_redirect_response=False,
        )
        self.assertFalse(Trip.objects.filter(pk=self.trip.pk).exists())

    def test_cannot_delete_another_users_trip(self):
        self.client.force_login(self.other)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Trip.objects.filter(pk=self.trip.pk).exists())

class AddActivityViewTests(TripsViewTestBase):
    def setUp(self):
        super().setUp()
        self.url = reverse("add_activity", args=[self.trip.id, self.day.id])
        self.valid = {
            "attraction_id": self.louvre.id,
            "start_time": "10:00",
            "end_time": "12:00",
        }

    def post_activity(self, payload):
        return self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_login_is_required(self):
        self.client.logout()

        response = self.post_activity(self.valid)

        self.assert_login_redirect(response, self.url)
        self.assertFalse(PlannedActivity.objects.exists())

    def test_other_users_trip_returns_404(self):
        self.client.force_login(self.other)

        response = self.post_activity(self.valid)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(PlannedActivity.objects.exists())

    def test_missing_fields_return_400(self):
        for missing in self.valid:
            with self.subTest(missing=missing):
                payload = {
                    key: value for key, value in self.valid.items() if key != missing
                }
                response = self.post_activity(payload)

                self.assertEqual(response.status_code, 400)
                self.assertIn("Missing", response.json()["error"])

    def test_valid_post_creates_activity(self):
        response = self.post_activity(self.valid)

        self.assertEqual(response.status_code, 201)
        activity = response.json()["activity"]
        self.assertEqual(activity["attraction_id"], self.louvre.id)
        self.assertEqual(activity["start_time"], "10:00:00")
        self.assertEqual(activity["end_time"], "12:00:00")
        self.assertEqual(activity["order"], 1)
        self.assertEqual(activity["status"], "scheduled")
        self.assertIsNone(activity["notes"])
        self.assertEqual(PlannedActivity.objects.count(), 1)

@override_settings(WEATHER_API_KEY="")
class ItineraryBuilderViewTests(TripsViewTestBase):
    def setUp(self):
        super().setUp()
        self.url = reverse("itinerary_builder", args=[self.trip.id])

    def test_login_is_required(self):
        self.client.logout()
        self.assert_login_redirect(self.client.get(self.url), self.url)

    def test_other_users_trip_returns_404(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_renders_template_and_context(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/itinerary_builder.html")
        self.assertEqual(response.context["trip"], self.trip)

    def test_days_are_generated_for_whole_trip(self):
        data = self.client.get(self.url).context["app_data"]

        self.assertEqual(
            [day["day_number"] for day in data["days"]],
            [1, 2, 3, 4, 5],
        )
        self.assertEqual(self.trip.trip_days.count(), 5)

class GetDestinationWeatherTests(TestCase):
    @override_settings(WEATHER_API_KEY="test-key")
    @patch("trips.views.requests.get")
    def test_maps_weather_response(self, mock_get):
        mock_get.return_value.json.return_value = {
            "days": [
                {
                    "datetime": "2026-12-01",
                    "tempmax": 10,
                    "tempmin": 3,
                    "conditions": "Rain",
                    "precipprob": 80,
                    "icon": "rain",
                    "unrelated": "dropped",
                }
            ]
        }

        result = get_destination_weather(
            latitude=Decimal("48.856600"),
            longitude=Decimal("2.352200"),
            start_date=datetime.date(2026, 12, 1),
            end_date=datetime.date(2026, 12, 5),
        )

        self.assertEqual(
            result,
            [
                {
                    "date": "2026-12-01",
                    "tempmax": 10,
                    "tempmin": 3,
                    "conditions": "Rain",
                    "precipprob": 80,
                    "icon": "rain",
                }
            ],
        )

# Forms


class WizardFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.paris = make_destination()

    def test_preference_form(self):
        form = PreferenceWizardForm(data={"travel_style": "culture"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertFalse(form.cleaned_data["nightlife"])

    def test_preference_travel_style_is_required(self):
        form = PreferenceWizardForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("travel_style", form.errors)

    def test_destination_form(self):
        form = DestinationWizardForm(
            data={
                "destination": self.paris.id,
                "name": "Paris Break",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["destination"], self.paris)

    def test_destination_fields_are_required(self):
        form = DestinationWizardForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors), {"destination", "name"})

    def test_trip_details_form_accepts_future_dates(self):
        start = timezone.now().date() + datetime.timedelta(days=10)
        form = TripDetailsWizardForm(
            data={
                "start_date": start.isoformat(),
                "end_date": (start + datetime.timedelta(days=3)).isoformat(),
                "budget": "500.00",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_trip_details_form_rejects_past_start_date(self):
        today = timezone.now().date()
        start = today - datetime.timedelta(days=1)
        form = TripDetailsWizardForm(
            data={
                "start_date": start.isoformat(),
                "end_date": (today + datetime.timedelta(days=2)).isoformat(),
                "budget": "500.00",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["start_date"],
            ["Start date cannot be before today."],
        )

    def test_empty_review_form_is_valid(self):
        self.assertTrue(ReviewForm(data={}).is_valid())