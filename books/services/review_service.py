from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from books.models import Book, BookReview


def get_book_or_404(book_id: int) -> Book:
    return get_object_or_404(Book.objects.prefetch_related("book_authors__author"), id=book_id)


def get_book_review_or_404(book: Book, review_id: int) -> BookReview:
    return get_object_or_404(
        BookReview.objects.select_related("user", "book"),
        id=review_id,
        book=book,
    )


def add_review(*, book: Book, user, stars_given: int, comment: str) -> BookReview:
    return BookReview.objects.create(
        book=book,
        user=user,
        stars_given=stars_given,
        comment=comment,
    )


def update_review(*, review: BookReview, user, stars_given: int, comment: str) -> BookReview:
    if review.user_id != user.id:
        raise PermissionDenied("You cannot edit this review.")
    review.stars_given = stars_given
    review.comment = comment
    review.save(update_fields=["stars_given", "comment"])
    return review


def delete_review(*, review: BookReview, user) -> None:
    if review.user_id != user.id:
        raise PermissionDenied("You cannot delete this review.")
    review.delete()

