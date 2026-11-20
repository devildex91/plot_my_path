"""Permission helpers for free and premium trip creation."""

from .models import Trip

FREE_TRIP_LIMIT = 1


def is_premium(user):
    """Return whether the user has an active premium membership."""
    membership = getattr(user, "membership", None)
    return bool(membership and membership.is_active)


def can_create_trip(user):
    """Return whether the user may create another trip."""
    if user.is_staff or is_premium(user):
        return True
    return Trip.objects.filter(user=user).count() < FREE_TRIP_LIMIT
