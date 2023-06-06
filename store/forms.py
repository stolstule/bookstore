from django import forms

from .models import Review

class SearchForm(forms.Form):
    query = forms.CharField()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'book', 'content']

