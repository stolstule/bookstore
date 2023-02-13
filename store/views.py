from django.shortcuts import render
from django.views import View
from .models import Book

# Create your views here.


class MainPage(View):
    def get(self, request):
        pass

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