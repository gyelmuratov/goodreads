from django.core.paginator import Paginator

from books.models import BookReview


def get_home_feed_page(*, page: int = 1, page_size: int = 10):
    book_reviews = BookReview.objects.select_related("user", "book").order_by("-created_at", "-id")
    paginator = Paginator(book_reviews, page_size)
    return paginator.get_page(page)

