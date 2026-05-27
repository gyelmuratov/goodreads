from books.models import ReadingList


def get_user_reading_list_queryset(user, *, status: str | None = None):
    queryset = ReadingList.objects.filter(user=user).select_related("book").order_by("-updated_at", "-id")
    if status:
        queryset = queryset.filter(status=status)
    return queryset

