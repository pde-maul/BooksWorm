from django.contrib import admin
from .models import Book, Review, Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')

admin.site.register(Author, AuthorAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_title', 'book_rated', 'review_rate')
    list_filter = ('review_author', 'review_rate', 'book_rated')
    fieldsets = (
        (None, {
            'fields': ('review_title','book_rated', 'review_rate', 'review_author', 'review_text')
        }),
    )
