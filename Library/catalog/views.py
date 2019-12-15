from django.shortcuts import render, redirect
from catalog.models import Book, Author, Review
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author, Book, Review
from catalog.form import SignUpForm, CreateReviewForm
from django.db.models import F
from django.db.models import Avg
import collections

def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_reviews = Review.objects.all().count()
    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_reviews': num_reviews,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def SignupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def BookListView(request, sorted_by=''):
    model = Book
    
    if sorted_by == 'author':
        book_list = Book.objects.all().order_by('author')
    else: 
       book_list = Book.objects.all() 

    context ={
        'book_list': book_list,
        }
    return render(request, 'catalog/book_list.html', context=context)

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 2

class ReviewBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing reviews by current user."""
    model = Review
    template_name ='catalog/review_list_by_user.html'
    paginate_by = 2
    
    def get_queryset(self):
        return Review.objects.filter(review_author=self.request.user)

class ReviewDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic class-based view of a review"""
    model = Review

# Author management
class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    template_name ='catalog/author_form.html'
    fields = '__all__' # First way to list fiels

class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    template_name ='catalog/author_form.html'
    fields = ['first_name', 'last_name'] # Second way to list fiels

class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    template_name ='catalog/author_confirm_delete.html'
    success_url = reverse_lazy('authors')

# Book management
class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'year_publishing']

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'year_publishing']

class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')

# Review management
def ReviewCreate(request):
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.review_author = request.user
            review.save()

            book_list = Book.objects.all().filter(title=review.book_rated).first()

            book_list.total_rate()
            book_list.save()
            return redirect('my-reviews')
    else:
        form = CreateReviewForm()
    return render(request, 'catalog/review_form.html', {'form': form})

class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = '__all__'

class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('books')