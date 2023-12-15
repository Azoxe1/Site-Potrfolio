from string import Template

from django import forms
from .models import *


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Оставьте отзыв'}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'image']
