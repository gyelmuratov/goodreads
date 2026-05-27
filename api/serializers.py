
from rest_framework import serializers

from books.models import Author, Book, BookAuthor, BookReview, Favorite, ReadingList
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "username", "email")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "full_name", "bio")


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "description", "isbn", "cover_picture", "authors", "average_rating", "reviews_count")

    def get_authors(self, obj):
        # Use prefetched relations when available; fallback keeps serializer safe.
        relations = getattr(obj, "book_authors", None)
        if relations is None:
            relations = BookAuthor.objects.select_related("author").filter(book=obj)
        return [relation.author.full_name for relation in relations.all()]


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    # Kept for backward compatibility; request user is always enforced.
    user_id = serializers.IntegerField(write_only=True, required=False)
    book_id = serializers.PrimaryKeyRelatedField(source="book", queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = BookReview
        fields = ("id", "stars_given", "comment", "book", "user", "user_id", "book_id", "created_at")
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        # Enforce authenticated user ownership from request context.
        validated_data.pop("user_id", None)
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("user_id", None)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(source="book", queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "book", "book_id", "created_at")
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        favorite, _ = Favorite.objects.get_or_create(**validated_data)
        return favorite


class ReadingListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(source="book", queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = ReadingList
        fields = ("id", "book", "book_id", "status", "updated_at")
        read_only_fields = ("updated_at",)

    def create(self, validated_data):
        # Upsert by (user, book) so each book has one reading-list status per user.
        user = self.context["request"].user
        entry, _ = ReadingList.objects.update_or_create(
            user=user,
            book=validated_data["book"],
            defaults={"status": validated_data["status"]},
        )
        return entry

