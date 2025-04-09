from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    published_year = models.IntegerField()

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum([r.rating for r in reviews]) / len(reviews), 1)
        return None

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
