from django.urls import path
#from api.views import BookReviewDetailApiView, BookReviewsListApiView
from rest_framework.routers import DefaultRouter

from api.views import BookReviewsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('reviews', BookReviewsViewSet, basename='review')

urlpatterns = router.urls


# urlpatterns = [
#     path("reviews/", BookReviewsListApiView.as_view(), name="review-list"),
#     path("reviews/<int:id>/", BookReviewDetailApiView.as_view(), name="review-detail"),
#
# ]