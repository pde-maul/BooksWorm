from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from catalog.models import Book, Review


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('book_rated', 'review_title', 'review_text', 'review_rate', )
