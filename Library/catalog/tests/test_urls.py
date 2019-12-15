from django.urls import reverse, resolve

class TestUrls:
    def test_book_details(self):
         path = reverse('book-detail', kwargs={'pk':1})
         assert resolve(path).view_name == 'book-detail'
    
    def test_books_list(self):
        path = reverse('books')
        assert resolve(path).view_name == 'books'
