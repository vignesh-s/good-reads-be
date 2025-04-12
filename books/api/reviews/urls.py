from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .reviews_views import BookOtherReviewsAPIView, ReviewViewSet

router = DefaultRouter()
router.register(r"reviews", ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("books/<int:pk>/other-reviews/", BookOtherReviewsAPIView.as_view(), name="book-other-reviews"),
]
