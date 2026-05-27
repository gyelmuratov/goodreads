from django.shortcuts import render

from books.services.feed_service import get_home_feed_page


def landing_page(request):
    return render(request, 'landing.html')

def home_page(request):
    try:
        page_size = int(request.GET.get('page_size', 10))
    except (TypeError, ValueError):
        page_size = 10
    try:
        page_number = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        page_number = 1
    page_objects = get_home_feed_page(page=page_number, page_size=page_size)

    return render(request, 'home.html', {'page_obj': page_objects})