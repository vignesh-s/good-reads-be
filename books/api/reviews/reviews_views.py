from django.db import IntegrityError
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from books.models.book import Book
from books.models.review import Review

from .reviews_serializers import ReviewSerializer


class OtherReviewsPagination(PageNumberPagination):
    page_size = 2

class BookOtherReviewsAPIView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        user = request.user if request.user.is_authenticated else None
        reviews = book.reviews.exclude(user=user).order_by("-timestamp")

        paginator = OtherReviewsPagination()
        page = paginator.paginate_queryset(reviews, request)
        serialized = ReviewSerializer(page, many=True)
        return paginator.get_paginated_response(serialized.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError("You have already reviewed this book.")

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only edit your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        instance.delete()
