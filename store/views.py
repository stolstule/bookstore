import sys
sys.path.append("..users")
from users.models import Basket
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Book, Category, Review
from django.db.models import Max, Min, Q, Avg
from .forms import ReviewForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .serializers import BookSerializer
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

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


        if len(get_request) > 1:
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

            paginator = Paginator(books_by_genre, 30)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)

            return render(request, 'store/genre_page.html', {
                'page_obj': page_obj,
                'count_books': len(books_by_genre),
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

            paginator = Paginator(books_by_genre, 30)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)

            return render(request, 'store/genre_page.html', {
                'page_obj': page_obj,
                'count_books': len(books_by_genre),
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
        review_status = False
        if request.user.is_authenticated:
            if Basket.objects.filter(user=request.user, book=book):
                basket = True
            else:
                basket = False
            user_auth = True
            if Review.objects.filter(user=request.user, book=book):
                review_status = True
        else:
            user_auth = False
            basket = False
            if len(request.session.keys()) != 0:
                if book.id in request.session['basket']:
                    basket = True
                else:
                    basket = False
            else:
                request.session['basket'] = []
        reviews = Review.objects.filter(book=book)
        form = ReviewForm()
        if reviews.values('rating').aggregate(Avg('rating'))['rating__avg']:
            rating_book = reviews.values('rating').aggregate(Avg('rating'))['rating__avg']
            get_book = Book.objects.get(id=book.id)
            get_book.rating = rating_book
            get_book.count_review = len(reviews)
            get_book.save()

        else:
            rating_book = 'Нет оценок'

        return render(request, 'store/book_page.html', {
            'count_reviews': len(reviews),
            'rating_book': rating_book,
            'review_status': review_status,
            'reviews': reviews,
            'user_auth': user_auth,
            'form': form,
            'book': book,
            'basket': basket,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })

    def post(self, request, slug_book):
        form = ReviewForm(request.POST)
        if form.is_valid():
            book_get = Book.objects.get(slug=slug_book)
            book_get.count_review = book_get.count_review + 1
            book_get.save()
            review = form.save(commit=False)
            review.user = request.user
            review.book = book_get
            review.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def search_page(request):
    if request.method == 'GET':
        search_field = request.GET.get('search_field', '')
        book_list = Book.objects.filter(Q(title__icontains=search_field) | Q(author__icontains=search_field))
        paginator = Paginator(book_list, 30)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'store/search_page.html', {
            'search_field': search_field,
            'page_obj': page_obj,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })
    else:
        return render(request, 'store/search_page.html', {
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })


def rating_books(request):
    if request.method == 'GET':
        book_list = Book.objects.all().order_by('rating')
        paginator = Paginator(book_list, 30)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'store/rating&popular_page.html', {
            'page_obj': page_obj,
            'label': 'rating',
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })

def popular_books(request):
    if request.method == 'GET':
        book_list = Book.objects.order_by('-count_review')
        paginator = Paginator(book_list, 30)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'store/rating&popular_page.html', {
            'label': 'popular',
            'page_obj': page_obj,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })

def random_book(request):
    book = Book.objects.order_by('?').first()
    return redirect('book_page', slug_book=book.slug)


class BookAPIList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class BookAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsOwnerOrReadOnly, )

class BookAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly, )