from django.urls import path

from .books_views import BookDetailAPIView, BookListAPIView

urlpatterns = [
    path("", BookListAPIView.as_view(), name="book-list"),
    path("<int:pk>/", BookDetailAPIView.as_view(), name="book-detail"),
]
