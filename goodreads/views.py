from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import BookReview


def landing_page(request):
    return render(request, 'landing.html')

def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at', '-id')
    page_size = request.GET.get('page_size',10)
    paginator = Paginator(book_reviews, int(page_size))

    page_number = request.GET.get('page',1)
    page_objects = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_objects})