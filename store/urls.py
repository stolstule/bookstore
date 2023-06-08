from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('search', views.search_page, name='search'),
    path('rating_books', views.rating_books, name='rating_books'),
    path('random_book', views.random_book, name='random_book'),
    path('popular_books', views.popular_books, name='popular_books'),
    path('book_page/<slug:slug_book>', views.BookPage.as_view(), name='book_page'),
    path('category/<slug:slug_genre>', views.ShowGenreBooks.as_view(), name='genre_page'),
]
