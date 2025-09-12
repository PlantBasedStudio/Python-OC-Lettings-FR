from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    User profile model extending Django's built-in User model.

    This model creates a one-to-one relationship with Django's User model
    to store additional user information that is not included in the default
    User model. Currently stores the user's favorite city preference.

    Attributes:
        user (OneToOneField): One-to-one relationship with Django's User model.
            When the associated User is deleted, this Profile will also be deleted
            due to CASCADE behavior.
        favorite_city (CharField): Optional field storing the user's preferred city.
            Limited to 64 characters and can be left blank.

    Methods:
        __str__(): Returns the username of the associated User for easy identification.

    Meta:
        db_table (str): Specifies the database table name as 'profiles_profile'
            for consistency with the application structure.

    Note:
        The CASCADE delete behavior ensures data integrity by removing
        orphaned profiles when users are deleted from the system.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """
        String representation of the Profile model.

        Returns:
            str: The username of the associated User object.
        """
        return self.user.username

    class Meta:
        db_table = "profiles_profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
