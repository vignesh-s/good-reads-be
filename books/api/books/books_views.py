from django.shortcuts import get_object_or_404
from rest_framework import filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from books.api.reviews.reviews_serializers import ReviewSerializer
from books.models.book import Book

from .books_serializers import BookDetailSerializer, BookListSerializer


class BookPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'

class BookListAPIView(generics.ListAPIView):
    serializer_class = BookListSerializer
    pagination_class = BookPagination
    queryset = Book.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'genre']

class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer

    def get(self, request, pk):
        book = self.get_object()
        user_review = None
        if request.user.is_authenticated:
            user_review = book.reviews.filter(user=request.user).first()

        return Response({
            "book": BookDetailSerializer(book).data,
            "user_review": ReviewSerializer(user_review).data if user_review else None,
        })
    