from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from transliterate import translit
from numpy import average



class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    section = models.CharField(max_length=50, null=False, blank=True)

    def save(self, *args, **kwargs):
        translit_slug = translit(self.name, language_code='ru', reversed=True).replace("'", "")
        self.slug = translit_slug
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

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
    publisher = models.CharField(max_length=50, default='NULL')

    rating_dict = []


    def set_rating(self, number):
        Book.rating_dict.append(number)
        self.rating = average(Book.rating_dict)

    def save(self, *args, **kwargs):
        translit_slug = translit(self.title, language_code='ru', reversed=True).replace("'", "")
        self.slug = translit_slug
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class User(models.Model):
    nickname = models.CharField(max_length=100, db_index=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(validators=[MinLengthValidator(5)], max_length=20)


    def __str__(self):
        return self.nickname


class Review(models.Model):
    content = models.TextField(max_length=500, blank=True)
    rating_review = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    number = models.AutoField(validators=[MinValueValidator(100)], primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book)


class Card(models.Model):
    number = models.CharField(max_length=16)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    date_year = models.IntegerField(validators=[MinValueValidator(datetime.now().year), MaxValueValidator(datetime.now().year + 5)])
    last_name = models.CharField(max_length=20)
    cvv = models.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(3)])
