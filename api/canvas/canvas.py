from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
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


def get_book_borrower_count(request, pk):
    month_dict = {
        'January': 0,
        'February': 0,
        'March': 0,
        'April': 0,
        'May': 0,
        'June': 0,
        'July': 0,
        'August': 0,
        'September': 0,
        'October': 0,
        'November': 0,
        'December': 0,
    }
    
    book = get_object_or_404(catalog_models.Book, pk=pk)
    
    book_inst_count_by_month = (
        catalog_models.BookInstance.objects
        .filter(book=book)
        .annotate(month=TruncMonth('due_back'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    for item in book_inst_count_by_month:
        month_name = item['month'].strftime('%B')  # 將日期轉換為月份名稱
        month_dict[month_name] = item['count']

    return JsonResponse(month_dict)