from django.utils import timezone

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    isbn = models.CharField(max_length=17, unique=True, db_index=True)
    cover_picture = models.URLField(null=True, blank=True)

    def get_cover(self):
        if self.cover_picture:
            return self.cover_picture
        return "https://picsum.photos/200/300"

    class Meta:
        ordering = ["id"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
        ]

    def __str__(self):
        return self.title


class ReadingStatus(models.TextChoices):
    WANT_TO_READ = "want_to_read", "Want to read"
    READING = "reading", "Reading"
    FINISHED = "finished", "Finished"


class Author(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True)
    bio = models.TextField()

    class Meta:
        ordering = ["last_name", "first_name", "id"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_authors")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="book_authors")

    class Meta:
        ordering = ["id"]
        verbose_name = "Book author relation"
        verbose_name_plural = "Book author relations"
        constraints = [
            models.UniqueConstraint(fields=["book", "author"], name="unique_book_author_relation"),
        ]
        indexes = [
            models.Index(fields=["book", "author"]),
            models.Index(fields=["author", "book"]),
        ]

    def __str__(self):
        return self.book.title + ' ' + self.author.first_name + ' ' + self.author.last_name

class BookReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "Book review"
        verbose_name_plural = "Book reviews"
        indexes = [
            models.Index(fields=["book", "-created_at"]),
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["book", "stars_given"]),
        ]

    def __str__(self):
        return f"{self.stars_given} stars of {self.book.title}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        constraints = [
            models.UniqueConstraint(fields=["user", "book"], name="unique_user_book_favorite"),
        ]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["book", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user} favorited {self.book}"


class ReadingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_list_entries")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reading_list_entries")
    status = models.CharField(max_length=20, choices=ReadingStatus.choices, default=ReadingStatus.WANT_TO_READ, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ["-updated_at", "-id"]
        verbose_name = "Reading list entry"
        verbose_name_plural = "Reading list entries"
        constraints = [
            models.UniqueConstraint(fields=["user", "book"], name="unique_user_book_reading_list"),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["book", "status"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.book} ({self.status})"

