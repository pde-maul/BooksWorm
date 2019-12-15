from catalog.models import Author
import pytest


@pytest.mark.django_db
class TestModelAuthor:

    def test_author_fields(self):
        Author.objects.create(first_name='Thomas', last_name='Cook')

        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        assert field_label == 'first name'

        max_length = author._meta.get_field('first_name').max_length
        assert max_length == 100
    
        expected_object_name = f'{author.first_name} {author.last_name}'
        assert expected_object_name == str(author)

        author = Author.objects.get(id=1)
        assert author.get_absolute_url() ==  '/catalog/author/1'