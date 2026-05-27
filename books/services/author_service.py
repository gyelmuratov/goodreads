from django.db.models import Prefetch

from books.models import Author, BookAuthor


def get_author_prefetch() -> Prefetch:
    return Prefetch(
        "book_authors",
        queryset=BookAuthor.objects.select_related("author"),
    )


def list_authors():
    return Author.objects.all().order_by("last_name", "first_name", "id")

