from django.core.paginator import Paginator
from django.db.models import Avg, Count, Prefetch, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

from books.models import Book, BookReview
from books.services.author_service import get_author_prefetch


MAX_PAGE_SIZE = 50


def _safe_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_page_size(page_size: int) -> int:
    # Guard against very large page sizes causing heavy DB/page memory load.
    return max(1, min(page_size, MAX_PAGE_SIZE))


def get_books_search_queryset(*, search_query: str = ""):
    # Add rating/review aggregates once so list/detail serializers stay efficient.
    queryset = Book.objects.prefetch_related(get_author_prefetch()).annotate(
        average_rating=Coalesce(Avg("reviews__stars_given"), 0.0),
        reviews_count=Count("reviews", distinct=True),
    )
    if search_query:
        # Search by title and author names without changing frontend contracts.
        queryset = queryset.filter(
            Q(title__icontains=search_query)
            | Q(book_authors__author__first_name__icontains=search_query)
            | Q(book_authors__author__last_name__icontains=search_query)
        )
    return queryset.order_by("id").distinct()


def list_books_page(*, search_query: str = "", page: int = 1, page_size: int = 2):
    queryset = get_books_search_queryset(search_query=search_query)
    paginator = Paginator(queryset, _normalize_page_size(page_size))
    return paginator.get_page(page)


def get_book_detail_or_404(book_id: int) -> Book:
    reviews_prefetch = Prefetch(
        "reviews",
        # Pull review users in the same query to avoid per-review user fetches.
        queryset=BookReview.objects.select_related("user").order_by("-created_at", "-id"),
    )
    # Prefetch both book_authors and reviews for detail page rendering.
    queryset = (
        Book.objects.prefetch_related(get_author_prefetch(), reviews_prefetch)
        .annotate(
            average_rating=Coalesce(Avg("reviews__stars_given"), 0.0),
            reviews_count=Count("reviews", distinct=True),
        )
    )
    return get_object_or_404(queryset, id=book_id)


def parse_books_list_params(request):
    search_query = request.GET.get("q", "").strip()
    page_size = _normalize_page_size(_safe_int(request.GET.get("page_size", 2), 2))
    page_number = _safe_int(request.GET.get("page", 1), 1)
    return search_query, page_number, page_size

