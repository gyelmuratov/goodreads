from django.contrib import admin
from django.db.models import Count

from books.models import Author, Book, BookAuthor, BookReview, Favorite, ReadingList


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ("title", "isbn")
    list_display = ("title", "isbn", "reviews_count")
    list_per_page = 25

    def get_queryset(self, request):
        # Annotate once so list rows do not trigger per-object count queries.
        return super().get_queryset(request).annotate(_reviews_count=Count("reviews"))

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
    # Pull related book/user in the changelist query to avoid N+1.
    list_select_related = ("book", "user")
    list_per_page = 50


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("book", "author")
    search_fields = ("book__title", "author__first_name", "author__last_name")
    # Pull both FK sides up front for admin list performance.
    list_select_related = ("book", "author")
    list_per_page = 50


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "created_at")
    search_fields = ("user__username", "book__title")
    list_select_related = ("user", "book")
    list_per_page = 50


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "status", "updated_at")
    search_fields = ("user__username", "book__title")
    list_filter = ("status",)
    list_select_related = ("user", "book")
    list_per_page = 50
