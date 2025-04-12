from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from books.models.book import Book
from books.models.review import Review


class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.book1 = Book.objects.create(
            title="Book One", author="Author A", genre="Fiction", published_year=2020
        )
        self.book2 = Book.objects.create(
            title="Book Two", author="Author B", genre="Sci-Fi", published_year=2021
        )
        self.review = Review.objects.create(
            book=self.book1, user=self.user, rating=4, comment="Nice book"
        )

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertTrue(any(b["title"] == "Book One" for b in response.data["results"]))

    def test_list_books_with_search(self):
        url = reverse("book-list") + "?search=Sci-Fi"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all("Sci-Fi" in b["genre"] for b in response.data["results"]))

    def test_retrieve_book_detail(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book"]["id"], self.book1.id)

    def test_book_detail_with_user_review(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_review"]["comment"], "Nice book")
