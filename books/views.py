from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View

from books.forms import BookReviewForm
from books.models import Book, BookReview
from books.services.review_service import (
    add_review,
    delete_review,
    get_book_or_404,
    get_book_review_or_404,
    update_review,
)


class BooksView(View):
    def get(self, request):
        books = Book.objects.prefetch_related("book_authors__author").order_by('id')
        search_query = request.GET.get('q', '')

        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size',2)
        paginator = Paginator(books, page_size)

        page_number = request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'books/list.html',
            {'page_obj': page_obj, 'search_query': search_query})


class BookDetailView(View):
    def get(self, request, id):
        review_prefetch = Prefetch(
            "reviews",
            queryset=BookReview.objects.select_related("user").order_by("-created_at", "-id"),
        )
        book = get_object_or_404(
            Book.objects.prefetch_related("book_authors__author", review_prefetch),
            id=id,
        )
        review_form = BookReviewForm()
        return render(
            request,
            'books/detail.html',
            {'book': book, 'review_form': review_form})


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
            {'book': book, 'review_form': review_form})


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