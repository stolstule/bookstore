from django.shortcuts import render
from django.views import View
from .models import Book, Category

# Create your views here.


class MainPage(View):
    def get(self, request):
        genre = ['Фантастика и фэнтези', 'Драмматургия', 'Приключения', 'Медицина и здоровье', 'Психология', 'Бизнес и экономика']
        dict_books = {}
        for i in genre:
            book_query = Book.objects.filter(category__name=i)
            dict_books[i] = book_query[len(book_query) - 5:]
        fantasy_books = dict_books['Фантастика и фэнтези']
        del dict_books['Фантастика и фэнтези']
        return render(request, 'store/main_page.html', {
            'fantasy_books': fantasy_books,
            'dict_other_books': dict_books
        })

class BasketAreaPage(View):
    pass

class PopularBooksPage(View):
    pass


class PersonalAreaPage(View):
    pass


class RandomBookPage(View):
    pass


class GenrePage(View):
    pass


class BookPage(View):
    pass

class RatingBooksPage(View):
    pass