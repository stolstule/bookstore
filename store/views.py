from django.shortcuts import render
from django.views import View
from .models import Book_check

# Create your views here.


class MainPage(View):
    def get(self, request):
        book = Book_check.objects.get(id=1)
        return render(request, 'store/main_page.html', context={'book': book})

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