from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models.book import Book
from books.models.review import Review


class ReviewAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="password")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Review Book", author="Another Author", genre="Sci-Fi", published_year=2015
        )
        self.review = Review.objects.create(
            book=self.book, user=self.user, rating=5, comment="Excellent"
        )
        self.user2 = User.objects.create_user(username="reviewer2", password="password")

    def test_list_reviews_for_book(self):
        url = reverse("book-other-reviews", kwargs={"pk": self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

        self.review = Review.objects.create(
            book=self.book, user=self.user2, rating=4, comment="Nice"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_review(self):
        url = reverse("review-detail", args=[self.review.id])
        data = {"rating": 4, "comment": "Updated comment", "book": self.book.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, "Updated comment")

    def test_create_review_fails_if_already_exists(self):
        url = reverse("review-list")
        data = {"rating": 3, "comment": "Trying again", "book": self.book.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_review(self):
        url = reverse("review-detail", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_update_review_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("review-detail", args=[self.review.id])
        data = {"rating": 4, "comment": "Updated comment", "book": self.book.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("review-detail", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
