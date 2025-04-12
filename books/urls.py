from django.urls import include, path

urlpatterns = [
    path('books/', include('books.api.books.urls')),
    path('', include('books.api.reviews.urls')),
    path('', include('books.api.users.urls')),
]
