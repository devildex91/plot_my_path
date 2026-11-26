"""Models for countries, destinations, and attractions."""

from django.conf import settings
from django.db import models


class CountryManager(models.Manager):
    """Provide lookup helpers for country fixture data."""

    def get_by_natural_key(self, name):
        """Resolve fixture natural keys using the country's unique name."""
        return self.get(name=name)


class Country(models.Model):
    """Represent a country and its continent for destination browsing."""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, help_text="ISO country code")
    continent = models.CharField(max_length=50)

    objects = CountryManager()

    def natural_key(self):
        """Use the country name as the stable key when loading fixtures."""
        return (self.name,)

    def __str__(self):
        """Return the country name."""
        return self.name


class DestinationManager(models.Manager):
    """Provide lookup helpers for destination fixture data."""

    def get_by_natural_key(self, slug):
        """Resolve destination fixtures by their unique slug."""
        return self.get(slug=slug)


class Destination(models.Model):
    """A travel destination with coordinates, description, and estimated daily cost."""

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="destinations"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    average_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    objects = DestinationManager()

    # allows me to treat images like a database field when calling without storing image in db

    @property
    def get_image_url(self):
        """Build an automatically optimised Cloudinary URL."""
        cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "dxhclnrp")

        return (
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"c_limit,w_1080,q_auto,f_auto/"
            f"v1/{self.slug}"
        )

    @property
    def get_image_url_srcset(self):
        """Build responsive image URLs for different screen sizes."""
        cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "dxhclnrp")

        widths = [384, 576, 768, 1080]

        return ", ".join(
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"c_limit,w_{width},q_auto,f_auto/v1/{self.slug} {width}w"
            for width in widths
        )

    def natural_key(self):
        """Use the unique slug as the stable key when loading fixtures."""
        return (self.slug,)

    def __str__(self):
        """Return the destination name."""
        return self.name


class Attraction(models.Model):
    """A place of interest that can be shown or scheduled within a destination."""

    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="attractions"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    category = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    average_visit_minutes = models.IntegerField()
    entry_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    opening_time = models.TimeField(auto_now=False, auto_now_add=False)
    closing_time = models.TimeField(auto_now=False, auto_now_add=False)

    class Meta:
        unique_together = ("destination", "slug")

    @property
    def get_image_url(self):
        """Build an optimised Cloudinary image URL for this attraction."""
        cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "dxhclnrp")

        return (
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"c_limit,w_1080,q_auto,f_auto/"
            f"v1/{self.slug}"
        )

    @property
    def get_image_url_srcset(self):
        """Generate responsive Cloudinary image URLs."""
        cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "dxhclnrp")

        widths = [384, 576, 768, 1080]

        return ", ".join(
            f"https://res.cloudinary.com/{cloud_name}/image/upload/"
            f"c_limit,w_{width},q_auto,f_auto/v1/{self.slug} {width}w"
            for width in widths
        )

    def __str__(self):
        """Return the attraction name."""
        return self.name
