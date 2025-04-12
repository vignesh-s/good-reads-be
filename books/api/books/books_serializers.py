from rest_framework import serializers

from books.api.reviews.reviews_serializers import ReviewSerializer
from books.models.book import Book


class BookListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'published_year', 'average_rating']

class BookDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'published_year', 'average_rating']

