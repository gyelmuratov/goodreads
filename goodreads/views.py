from django.shortcuts import render

from books.services.feed_service import get_home_feed_page_from_request


def landing_page(request):
    return render(request, 'landing.html')

def home_page(request):
    page_objects = get_home_feed_page_from_request(request)

    return render(request, 'home.html', {'page_obj': page_objects})