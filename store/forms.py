from django import forms

from .models import Review

class SearchForm(forms.Form):
    query = forms.CharField()

