from rest_framework import viewsets
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from rest_framework.filters import SearchFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['genre', 'author']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
