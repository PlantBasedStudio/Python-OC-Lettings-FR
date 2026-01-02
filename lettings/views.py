"""
Views for the lettings application.

This module contains views for displaying property lettings,
including the listings index and individual letting details.
"""

import logging

from django.shortcuts import render, get_object_or_404
from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """
    Display a list of all available lettings.

    Retrieves all letting records from the database and renders them
    in the lettings index template. This view serves as the main
    listing page for property rentals.

    Args:
        request (HttpRequest): The HTTP request object containing
            metadata about the request.

    Returns:
        HttpResponse: Rendered HTML response containing the lettings
            index page with a list of all available lettings.

    Template:
        lettings/index.html: Template used to display the lettings list.

    Context:
        lettings_list (QuerySet): All Letting objects from the database.
    """
    lettings_list = Letting.objects.all()
    logger.info("Lettings index accessed - %d lettings found", len(lettings_list))
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


def letting(request, letting_id):
    """
    Display detailed information for a specific letting.

    Retrieves a single letting record by its ID and displays
    its details including title and associated address information.

    Args:
        request (HttpRequest): The HTTP request object containing
            metadata about the request.
        letting_id (int): The unique identifier of the letting
            to be displayed.

    Returns:
        HttpResponse: Rendered HTML response containing the letting
            detail page with title and address information.

    Raises:
        Letting.DoesNotExist: If no letting exists with the given ID.

    Template:
        letting.html: Template used to display the letting details.

    Context:
        title (str): The title of the letting.
        address (Address): The Address object associated with the letting.

    Note:
        Uses get_object_or_404() for proper error handling when letting doesn't exist.
    """
    logger.info("Letting detail accessed - ID: %d", letting_id)
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "lettings/letting.html", context)
