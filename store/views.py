import sys
sys.path.append("..users")
from users.models import Basket
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Book, Category
from django.db.models import Max, Min, Q, F

# Create your views here.
hud_genre_navbar = Category.objects.filter(section='Художественная литература')
nehud_genre_navbar = Category.objects.filter(section='Нехудожественная литература')


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
        all_publishers = []
        all_authors = []
        for book in books_by_genre:
            if book.author not in all_authors:
                all_authors.append(book.author)
            if book.publisher not in all_publishers:
                all_publishers.append(book.publisher)
        if genre.section == 'Художественная литература':
            genre_list = hud_genre_navbar
        else:
            genre_list = nehud_genre_navbar
        get_request = request.GET
        if len(get_request) > 0:
            if len(get_request['author']) > 0 and len(get_request['publisher']) > 0:
                books_by_genre = books_by_genre.filter(author__iexact=get_request['author']).filter(publisher__iexact=get_request['publisher'])
            elif len(get_request['author']) > 0 and len(get_request['publisher']) == 0:
                books_by_genre = books_by_genre.filter(author__iexact=get_request['author'])
            elif len(get_request['author']) == 0 and len(get_request['publisher']) > 0:
                books_by_genre = books_by_genre.filter(publisher__iexact=get_request['publisher'])

            if len(get_request['price_from']) > 0 and len(get_request['price_to']) > 0:
                books_by_genre = books_by_genre.filter(price__range=(get_request['price_from'], get_request['price_to']))
            elif len(get_request['price_from']) == 0 and len(get_request['price_to']) > 0:
                books_by_genre = books_by_genre.filter(price__range=(0, get_request['price_to']))
            elif len(get_request['price_from']) > 0 and len(get_request['price_to']) == 0:
                books_by_genre = books_by_genre.filter(price__range=(get_request['price_from'], Book.objects.aggregate(Max('price'))['price__max']))

            if len(get_request['volume_from']) > 0 and len(get_request['volume_to']) > 0:
                books_by_genre = books_by_genre.filter(volume__range=(get_request['volume_from'], get_request['volume_to']))
            elif len(get_request['volume_from']) == 0 and len(get_request['volume_to']) > 0:
                books_by_genre = books_by_genre.filter(volume__range=(0, get_request['volume_to']))
            elif len(get_request['volume_from']) > 0 and len(get_request['volume_to']) == 0:
                books_by_genre = books_by_genre.filter(volume__range=(get_request['volume_from'], Book.objects.aggregate(Max("volume"))['volume__max']))

            return render(request, 'store/genre_page.html', {
                'count_books': len(books_by_genre),
                'books_by_genre': books_by_genre,
                'genre_name': genre_name,
                'hud_genre_navbar': hud_genre_navbar,
                'nehud_genre_navbar': nehud_genre_navbar,
                'genre_list': genre_list,
                'all_authors': sorted(all_authors),
                'all_publishers': sorted(all_publishers),
                'author_field': get_request['author'],
                'publisher_field': get_request['publisher'],
                'price_from_field': get_request['price_from'],
                'price_to_field': get_request['price_to'],
                'volume_from_field': get_request['volume_from'],
                'volume_to_field': get_request['volume_to'],
                'price_min': Book.objects.aggregate(Min('price'))['price__min'],
                'price_max': Book.objects.aggregate(Max('price'))['price__max'],
                'volume_min': Book.objects.aggregate(Min("volume"))['volume__min'],
                'volume_max': Book.objects.aggregate(Max("volume"))['volume__max'],
            })
        else:
            return render(request, 'store/genre_page.html', {
                'count_books': len(books_by_genre),
                'books_by_genre': books_by_genre,
                'genre_name': genre_name,
                'hud_genre_navbar': hud_genre_navbar,
                'nehud_genre_navbar': nehud_genre_navbar,
                'genre_list': genre_list,
                'all_authors': sorted(all_authors),
                'all_publishers': sorted(all_publishers),
                'price_min': Book.objects.aggregate(Min('price'))['price__min'],
                'price_max': Book.objects.aggregate(Max('price'))['price__max'],
                'volume_min': Book.objects.aggregate(Min("volume"))['volume__min'],
                'volume_max': Book.objects.aggregate(Max("volume"))['volume__max'],
            })

class BookPage(View):
    def get(self, request, slug_book):
        book = get_object_or_404(Book, slug=slug_book)
        if request.user.is_authenticated:
            if Basket.objects.filter(user=request.user, book=book):
                basket = True
            else:
                basket = False
        else:
            basket = False
            if len(request.session.keys()) != 0:
                if book.id in request.session['basket']:
                    basket = True
                else:
                    basket = False
            else:
                request.session['basket'] = []

        return render(request, 'store/book_page.html', {
            'book': book,
            'basket': basket,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })


def search_page(request):
    if request.method == 'GET':
        search_field = request.GET.get('search_field', '')
        book_list = Book.objects.filter(Q(title__icontains=search_field) | Q(author__icontains=search_field))
        return render(request, 'store/search_page.html', {
            'search_field': search_field,
            'book_list': book_list,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })
    else:
        return render(request, 'store/search_page.html', {
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })


class BasketAreaPage(View):
    pass

class PopularBooksPage(View):
    pass

class RandomBookPage(View):
    pass

class RatingBooksPage(View):
    pass
