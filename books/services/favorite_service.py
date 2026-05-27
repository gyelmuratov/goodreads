from books.models import Favorite


def get_user_favorites_queryset(user):
    # Pull related book once for nested serializers.
    return Favorite.objects.filter(user=user).select_related("book").order_by("-created_at", "-id")

