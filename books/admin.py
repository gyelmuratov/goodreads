from django.contrib import admin
from django.db.models import Count

from books.models import Author, Book, BookAuthor, BookReview


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ("title", "isbn")
    list_display = ("title", "isbn", "reviews_count")
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _reviews_count=Count("reviews")
        )

    @admin.display(ordering="_reviews_count", description="Reviews")
    def reviews_count(self, obj):
        return obj._reviews_count


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name", "email")
    list_display = ("first_name", "last_name", "email")
    list_per_page = 25


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "stars_given", "created_at")
    search_fields = ("book__title", "user__username", "comment")
    list_select_related = ("book", "user")
    list_per_page = 50


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("book", "author")
    search_fields = ("book__title", "author__first_name", "author__last_name")
    list_select_related = ("book", "author")
    list_per_page = 50