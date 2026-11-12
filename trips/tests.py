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


from .models import PlannedActivity, Trip, TripDay, Recommendation


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
