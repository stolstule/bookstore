from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Book, Category

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
        genre_name = get_object_or_404(Category, slug=slug_genre)
        genre_name = genre_name.name
        books_by_genre = Book.objects.filter(category__name=genre_name)
        return render(request, 'store/genre_page.html', {
            'books_by_genre': books_by_genre,
            'genre_name': genre_name,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
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