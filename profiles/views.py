import logging

from django.shortcuts import render, get_object_or_404
from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """
    Display a list of all user profiles.

    Retrieves all profile records from the database and renders them
    in the profiles index template. This view serves as the main
    listing page for user profiles.

    Args:
        request (HttpRequest): The HTTP request object containing
            metadata about the request.

    Returns:
        HttpResponse: Rendered HTML response containing the profiles
            index page with a list of all available user profiles.

    Template:
        profiles/index.html: Template used to display the profiles list.

    Context:
        profiles_list (QuerySet): All Profile objects from the database.
    """
    profiles_list = Profile.objects.all()
    logger.info("Profiles index accessed - %d profiles found", len(profiles_list))
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)


def profile(request, username):
    """
    Display detailed information for a specific user profile.

    Retrieves a single profile record by the associated username and displays
    the user's profile information including their favorite city.

    Args:
        request (HttpRequest): The HTTP request object containing
            metadata about the request.
        username (str): The username of the user whose profile
            is to be displayed.

    Returns:
        HttpResponse: Rendered HTML response containing the profile
            detail page with user information.

    Raises:
        Http404: If no profile exists for the given username.

    Template:
        profile.html: Template used to display the profile details.

    Context:
        profile (Profile): The Profile object associated with the username.
    """
    logger.info("Profile detail accessed - username: %s", username)
    profile = get_object_or_404(Profile, user__username=username)
    context = {"profile": profile}
    return render(request, "profiles/profile.html", context)
