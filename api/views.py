from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    AuthorSerializer,
    BookReviewSerializer,
    BookSerializer,
    FavoriteSerializer,
    ReadingListSerializer,
)
from books.models import Author
from books.services.book_service import get_books_search_queryset
from books.services.favorite_service import get_user_favorites_queryset
from books.services.reading_list_service import get_user_reading_list_queryset
from books.services.review_service import get_reviews_queryset


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class BooksViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    pagination_class = DefaultPageNumberPagination
    filter_backends = [filters.SearchFilter]
    # Search by title and author names.
    search_fields = ["title", "book_authors__author__first_name", "book_authors__author__last_name"]

    def get_queryset(self):
        # Annotated and prefetch-optimized queryset from services layer.
        return get_books_search_queryset()


class AuthorsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    pagination_class = DefaultPageNumberPagination
    queryset = Author.objects.all().order_by("last_name", "first_name", "id")


class BookReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = BookReviewSerializer
    pagination_class = DefaultPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        return get_reviews_queryset()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPageNumberPagination
    lookup_field = "id"

    def get_queryset(self):
        # Users only see and mutate their own favorites.
        return get_user_favorites_queryset(self.request.user)


class ReadingListViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPageNumberPagination
    lookup_field = "id"

    def get_queryset(self):
        status = self.request.query_params.get("status")
        # Users only see and mutate their own reading-list entries.
        return get_user_reading_list_queryset(self.request.user, status=status)



# class BookReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all()
#     lookup_field = 'id'
#
#
#     # def get(self, request, id):
#     #     book_review = BookReview.objects.get(id=id)
#     #     serializer = BookReviewSerializer(book_review)
#     #     return Response(serializer.data)
#     #
#     # def delete(self, request, id):
#     #     book_review = BookReview.objects.get(id=id)
#     #     book_review.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
#     #
#     # def put(self, request, id):
#     #     book_review = BookReview.objects.get(id=id)
#     #     serializer = BookReviewSerializer(book_review, data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data,status=status.HTTP_200_OK)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     #
#     # def patch(self, request, id):
#     #     book_review = BookReview.objects.get(id=id)
#     #     serializer = BookReviewSerializer(book_review, data=request.data, partial=True)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data,status=status.HTTP_200_OK)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
# class BookReviewsListApiView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all().order_by('-id')
#
#
#
#     # def get(self, request):
#     #     book_reviews = BookReview.objects.all().order_by('-id')
#     #
#     #     paginator = PageNumberPagination()
#     #     page_obj = paginator.paginate_queryset(book_reviews, request)
#     #
#     #     serializer = BookReviewSerializer(page_obj, many=True)
#     #     return paginator.get_paginated_response(serializer.data)
#     #
#     # def post(self, request):
#     #     serializer = BookReviewSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)