from django.core.paginator import Paginator

from books.models import BookReview


MAX_FEED_PAGE_SIZE = 50


def _safe_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_home_feed_page(*, page: int = 1, page_size: int = 10):
    # Fetch related book/user in one hit for feed card rendering.
    book_reviews = BookReview.objects.select_related("user", "book").order_by("-created_at", "-id")
    safe_page_size = max(1, min(page_size, MAX_FEED_PAGE_SIZE))
    paginator = Paginator(book_reviews, safe_page_size)
    return paginator.get_page(page)


def get_home_feed_page_from_request(request):
    page_size = _safe_int(request.GET.get("page_size", 10), 10)
    page_number = _safe_int(request.GET.get("page", 1), 1)
    return get_home_feed_page(page=page_number, page_size=page_size)

