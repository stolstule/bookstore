from django import forms

from .models import Review

class SearchForm(forms.Form):
    query = forms.CharField()

class ReviewForm(forms.ModelForm):
    CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Review
        fields = ['content', 'rating']
