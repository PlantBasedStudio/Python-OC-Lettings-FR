from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """
    Model representing a physical address for property listings.

    This model stores complete address information including street address,
    city, state, postal code, and country. It enforces validation rules
    for proper address formatting and data integrity.

    Attributes:
        number (PositiveIntegerField): Street number, must be between 1-9999.
        street (CharField): Street name, maximum 64 characters.
        city (CharField): City name, maximum 64 characters.
        state (CharField): State abbreviation, exactly 2 characters.
        zip_code (PositiveIntegerField): Postal code, must be between 1-99999.
        country_iso_code (CharField): ISO country code, exactly 3 characters.

    Note:
        This model uses a custom database table name 'lettings_address'
        for legacy compatibility reasons.
    """

    number = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999)], help_text="Street number (1-9999)"
    )
    street = models.CharField(max_length=64, help_text="Street name")
    city = models.CharField(max_length=64, help_text="City name")
    state = models.CharField(
        max_length=2,
        validators=[MinLengthValidator(2)],
        help_text="State abbreviation (exactly 2 characters)",
    )
    zip_code = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999)], help_text="Postal/ZIP code (1-99999)"
    )
    country_iso_code = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(3)],
        help_text="ISO country code (exactly 3 characters)",
    )

    class Meta:
        db_table = "lettings_address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Letting(models.Model):
    """
    Model representing a property letting/rental listing.

    This model stores information about rental properties, linking each
    letting to a specific address. Each letting has a unique title and
    is associated with exactly one address through a one-to-one relationship.

    Attributes:
        title (CharField): Descriptive title for the letting, maximum 256 characters.
        address (OneToOneField): Reference to the associated Address object.

    Note:
        This model uses a custom database table name 'lettings_letting'
        for legacy compatibility reasons. When an Address is deleted,
        the associated Letting will also be deleted (CASCADE).
    """

    title = models.CharField(
        max_length=256, help_text="Descriptive title for the property letting"
    )
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        help_text="Associated address for this letting",
    )

    class Meta:
        db_table = "lettings_letting"
        verbose_name = "Letting"
        verbose_name_plural = "Lettings"
        ordering = ["title"]
