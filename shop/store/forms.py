from django import forms

from store.models import ReviewRating, CustomerQuestion


class ReviewForm(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['review', 'rating']


class QuestionForm(forms.ModelForm):

    class Meta:
        model = CustomerQuestion
        fields = ['question', 'name', 'email']
