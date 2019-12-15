from django.db import models
from django.core.validators  import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
import statistics
from django.db.models import Avg

class Review(models.Model):
    """Model representing a review for a book."""
    book_rated = models.ForeignKey('Book', on_delete=models.CASCADE)
    review_title = models.CharField(max_length=200, help_text='Enter a title for your review')
    review_text = models.TextField(max_length=300, help_text='Enter a brief review of the book', null=True, blank=True)
    review_rate = models.IntegerField(validators=[MaxValueValidator(5, "The rate has to be between 0 and 5"), MinValueValidator(0, "The rate has to be between 0 and 5")])
    review_author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        permissions = (("can_delete_review", "Delete their own review"),)   
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('review-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.review_title


class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book', null=True, blank=True)
    year_publishing = models.IntegerField('year published', validators=[MaxValueValidator(int(datetime.datetime.now().year)), MinValueValidator(1440, "Books didn't existe that early")])
    rating = models.FloatField('Average rate', default=0)

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def total_rate(self):
        review = Review.objects.all().filter(book_rated__title=self.title)

        if review:
            average_rate = review.aggregate(Avg('review_rate'))
            self.rating = round(average_rate['review_rate__avg'], 2)
            print("------------------------")
            print("self.rating", self.rating)
            return self.rating
        return 

    class Meta:
        ordering = ["-rating"]

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'