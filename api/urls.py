from rest_framework.routers import DefaultRouter

from api.views import AuthorsViewSet, BookReviewsViewSet, BooksViewSet, FavoriteViewSet, ReadingListViewSet

app_name = 'api'

router = DefaultRouter()
router.register("books", BooksViewSet, basename="book")
router.register("authors", AuthorsViewSet, basename="author")
router.register("reviews", BookReviewsViewSet, basename="review")
router.register("favorites", FavoriteViewSet, basename="favorite")
router.register("reading-list", ReadingListViewSet, basename="reading-list")

urlpatterns = router.urls