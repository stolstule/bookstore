from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('rating_books', views.RatingBooksPage.as_view(), name='rating_books'),
    path('random_book', views.RandomBookPage.as_view(), name='random_book'),
    path('popular_books', views.PopularBooksPage.as_view(), name='popular_books'),
    path('personal_area', views.PersonalAreaPage.as_view(), name='personal_area'),
    path('<slug:slug_genre>', views.ShowGenreBooks.as_view(), name='genre_page'),
    # path('<slug:slug_book>', views.BookPage, name='book_page'),
    path('basket', views.BasketAreaPage.as_view(), name='basket_page')
]
