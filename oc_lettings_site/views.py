from django.shortcuts import render


def index(request):
    """
    Display the home page of the OC Lettings site.

    Renders the main landing page that provides navigation
    to lettings and profiles sections of the application.

    Args:
        request (HttpRequest): The HTTP request object containing
            metadata about the request.

    Returns:
        HttpResponse: Rendered HTML response containing the home page.

    Template:
        index.html: Main template for the site's landing page.
    """
    return render(request, "index.html")


def custom_404_view(request, exception):
    """
    Custom 404 error page view.

    Handles Page Not Found errors by rendering a user-friendly
    error page instead of Django's default 404 page.

    Args:
        request (HttpRequest): The HTTP request object that resulted in 404.
        exception (Http404): The exception that triggered this error handler.

    Returns:
        HttpResponse: Rendered HTML response with 404 status code containing
            a custom error page with helpful information for the user.

    Template:
        404.html: Custom template for 404 error pages.
    """
    return render(request, "404.html", status=404)


def custom_500_view(request):
    """
    Custom 500 error page view.

    Handles Internal Server Error by rendering a user-friendly
    error page instead of Django's default 500 page.

    Args:
        request (HttpRequest): The HTTP request object that resulted in 500 error.

    Returns:
        HttpResponse: Rendered HTML response with 500 status code containing
            a custom error page with helpful information for the user.

    Template:
        500.html: Custom template for 500 error pages.
    """
    return render(request, "500.html", status=500)
