from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('rating_books', views.RatingBooksPage, name='rating_books'),
    path('random_book', views.RandomBookPage, name='random_book'),
    path('popular_books', views.PopularBooksPage, name='popular_books'),
    path('personal_area', views.PersonalAreaPage, name='personal_area'),
    path('<slug:slug_genre>', views.show_genre_books, name='genre_page'),
    # path('<slug:slug_book>', views.BookPage, name='book_page'),
    path('basket', views.BasketAreaPage, name='basket_page')
]
