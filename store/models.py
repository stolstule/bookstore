from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from transliterate import translit
from numpy import average


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    section = models.CharField(max_length=50, null=False, blank=True)


    def save(self, *args, **kwargs):
        translit_slug = translit(self.name, language_code='ru', reversed=True)
        self.slug = slugify(translit_slug)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('genre_page', args=[self.slug])

class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.CharField(max_length=200, null=False, blank=True)
    category = models.ManyToManyField(Category)
    isbn = models.CharField(max_length=30, default='NULL')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    price = models.IntegerField(default=0)
    image = models.FileField(max_length=1000, default='NULL')
    rating = models.FloatField(default=0)
    volume = models.IntegerField(default=0)
    description = models.TextField(max_length=4000, default='Без описания')
    publisher = models.CharField(max_length=200, default='NULL')
    rating = models.IntegerField(default=0, null=True, blank=True)


    def save(self, *args, **kwargs):
        translit_slug = translit(self.title, language_code='ru', reversed=True)
        self.slug = slugify(translit_slug)
        super(Book, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('book_page', args=[self.slug])

class Review(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    content = models.TextField(max_length=600)
    rating = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_review')
        ]
