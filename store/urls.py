from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('search', views.search_page, name='search'),
    path('rating_books', views.RatingBooksPage.as_view(), name='rating_books'),
    path('random_book', views.RandomBookPage.as_view(), name='random_book'),
    path('popular_books', views.PopularBooksPage.as_view(), name='popular_books'),
    path('book_page/<slug:slug_book>', views.BookPage.as_view(), name='book_page'),
    path('category/<slug:slug_genre>', views.ShowGenreBooks.as_view(), name='genre_page'),
]
