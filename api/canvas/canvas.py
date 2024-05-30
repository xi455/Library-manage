from django.http import HttpResponse, JsonResponse

from catalog import models as catalog_models


def get_genres():
    return catalog_models.Genre.objects.all()


def get_books():
    return catalog_models.Book.objects.all()


def get_book_instances():
    return catalog_models.BookInstance.objects.all()


def get_authors():
    return catalog_models.Author.objects.all()


def get_genres_book_count(request):
    queryset = catalog_models.Genre.objects.all()
    data = {genre.name: genre.book_set.count() for genre in queryset.distinct()}

    return JsonResponse(data)


def get_authors_book_count(request):
    queryset = catalog_models.Author.objects.all()
    data = {
        f"{author.first_name}, {author.last_name}": author.book_set.count()
        for author in queryset.distinct()
    }

    return JsonResponse(data)
