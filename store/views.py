from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Book, Category
from django.db.models import Max, Min

# Create your views here.
hud_genre_navbar = Category.objects.filter(section='Художественная литература')
nehud_genre_navbar = Category.objects.filter(section='Нехудожественная литература')
all_books = Book.objects.all()
all_publishers = []
all_authors = []
for book in all_books:
    if book.author not in all_authors:
        all_authors.append(book.author)
    if book.publisher not in all_publishers:
        all_publishers.append(book.publisher)

price_min =  Book.objects.aggregate(Min("price"))

class MainPage(View):
    def get(self, request):
        genre = Category.objects.all()
        dict_books = {}
        for i in genre:
            book_query = Book.objects.filter(category__name=i.name)
            dict_books[i.name] = book_query[len(book_query) - 5:]
        fantasy_books = dict_books['Фантастика и фэнтези']
        del dict_books['Фантастика и фэнтези']
        return render(request, 'store/main_page.html', {
            'fantasy_books': fantasy_books,
            'dict_other_books': dict_books,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })

class ShowGenreBooks(View):
    def get(self, request, slug_genre):
        genre = get_object_or_404(Category, slug=slug_genre)
        genre_name = genre.name
        books_by_genre = Book.objects.filter(category__name=genre_name)
        if genre.section == 'Художественная литература':
            genre_list = hud_genre_navbar
        else:
            genre_list = nehud_genre_navbar
        # request = request.GET()
        # if len(request) > 0:
        #     request = request.GET()
        #     books_by_genre = books_by_genre.filter(author__iexact=request['author']).filter(publisher_iexact=request['publisher'])
        #     if len(request['price_from']) > 0 and len(request['price_to']) > 0:
        #         books_by_genre = books_by_genre.filter(price__range=(request['price_from'], request['price_to']))
        #     elif len(request['price_from']) < 1 and len(request['price_to']) > 0:
        #         books_by_genre = books_by_genre.filter(price__range=(0, request['price_to']))
        #     elif len(request['price_from']) > 0 and len(request['price_to']) < 1:
        #         books_by_genre = books_by_genre.filter(price__range=(request['price_to'], Book.objects.aggregate(Max("price"))))
        #
        #     if len(request['volume_from']) > 0 and len(request['volume_to']) > 0:
        #         books_by_genre = books_by_genre.filter(volume__range=(request['volume_from'], request['volume_to']))
        #     elif len(request['volume_from']) < 1 and len(request['volume_to']) > 0:
        #         books_by_genre = books_by_genre.filter(volume__range=(0, request['volume_to']))
        #     elif len(request['volume_from']) > 0 and len(request['volume_to']) < 1:
        #         books_by_genre = books_by_genre.filter(volume__range=(request['volume_to'], Book.objects.aggregate(Max("volume"))))

        return render(request, 'store/genre_page.html', {
            'books_by_genre': books_by_genre,
            'genre_name': genre_name,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar,
            'genre_list': genre_list,
            'all_authors': sorted(all_authors),
            'all_publishers': sorted(all_publishers),
            'price_min': price_min,
            'price_max': Book.objects.aggregate(Max("price")),
            'volume_min': Book.objects.aggregate(Min("volume")),
            'volume_max': Book.objects.aggregate(Max("price")),
        })

# def show_genre_books(request, slug_genre:str):
#     genre_name = Category.objects.get(slug=slug_genre)
#     genre_name = genre_name.name
#     books_by_genre = Book.objects.filter(category__name=genre_name)
#     return render(request, 'store/genre_page.html', {
#         'books_by_genre': books_by_genre,
#         'genre_name': genre_name
#     })

class BasketAreaPage(View):
    pass

class PopularBooksPage(View):
    pass


class PersonalAreaPage(View):
    pass


class RandomBookPage(View):
    pass


class BookPage(View):
    pass

class RatingBooksPage(View):
    pass