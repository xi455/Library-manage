from django.urls import path

from api.canvas import canvas

app_name = "canvas"
urlpatterns = [
    path("genres/", canvas.get_genres_book_count, name="get-genres-book-count"),
    path("authors/", canvas.get_authors_book_count, name="get-authors-book-count"),
    path("book-borrower-count/<pk>", canvas.get_book_borrower_count, name="get-book-borrower-count"),
]
