from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from books.forms import BookReviewForm
from books.services.book_service import (
    get_book_detail_or_404,
    list_books_page,
    parse_books_list_params,
)
from books.services.review_service import (
    add_review,
    delete_review,
    get_book_or_404,
    get_book_review_or_404,
    update_review,
)


class BooksView(View):
    def get(self, request):
        search_query, page_number, page_size = parse_books_list_params(request)
        page_obj = list_books_page(
            search_query=search_query,
            page=page_number,
            page_size=page_size,
        )
        return render(
            request,
            'books/list.html',
            {'page_obj': page_obj, 'search_query': search_query})


class BookDetailView(View):
    def get(self, request, id):
        book = get_book_detail_or_404(id)
        review_form = BookReviewForm()
        # Use prefetched list once; template reads these without extra relation checks.
        reviews = list(book.reviews.all())
        return render(
            request,
            'books/detail.html',
            {'book': book, 'review_form': review_form, 'reviews': reviews, 'has_reviews': bool(reviews)})


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = get_book_or_404(id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            add_review(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment'],
            )
            return redirect(reverse('books:detail', kwargs={'id': book.id}))
        return render(
            request,
            'books/detail.html',
            self._build_detail_context(id=id, review_form=review_form),
        )

    @staticmethod
    def _build_detail_context(*, id: int, review_form: BookReviewForm):
        # Reuse optimized detail fetch so invalid form re-render avoids N+1.
        detail_book = get_book_detail_or_404(id)
        reviews = list(detail_book.reviews.all())
        return {
            "book": detail_book,
            "review_form": review_form,
            "reviews": reviews,
            "has_reviews": bool(reviews),
        }


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = get_book_or_404(book_id)
        review = get_book_review_or_404(book, review_id)
        review_form = BookReviewForm(instance=review)

        return render(
            request,
            "books/edit_review.html",
            {'book': book, 'review': review,
             'review_form': review_form})

    def post(self, request, book_id, review_id):
        book = get_book_or_404(book_id)
        review = get_book_review_or_404(book, review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            update_review(
                review=review,
                user=request.user,
                stars_given=review_form.cleaned_data["stars_given"],
                comment=review_form.cleaned_data["comment"],
            )
            return redirect(reverse('books:detail', kwargs={'id': book_id}))
        return render(
            request,
            "books/edit_review.html",
            {'book': book, 'review': review,
             'review_form': review_form})

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = get_book_or_404(book_id)
        review = get_book_review_or_404(book, review_id)

        return render(request,
                      'books/confirm_delete_review.html',
                      {'book':book, 'review': review})


class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, book_id, review_id):
        book = get_book_or_404(book_id)
        review = get_book_review_or_404(book, review_id)

        delete_review(review=review, user=request.user)
        messages.success(request, 'Review deleted successfully')

        return redirect(reverse('books:detail', kwargs={'id': book_id}))