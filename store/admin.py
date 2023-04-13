import sys
sys.path.append("..users")
from django.contrib import admin
from .models import  Book, Category
from users.models import Profile

admin.site.register(Profile)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'author', 'publisher')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')