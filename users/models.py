import sys
sys.path.append("..store")
from django.db import models
from django.contrib.auth.models import User
from store.models import Book


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='img/user.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.book.title}'

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.User)
        return
# Create your models here.
