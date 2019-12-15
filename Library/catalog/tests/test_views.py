from django.urls import reverse
from django.test import RequestFactory 
from catalog.views import AuthorListView
from catalog.models import Author
import pytest

@pytest.mark.django_db
class TestAuthorListView:

    def test_author_list(self):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Thomas {author_id}',
                last_name=f'Cook {author_id}',
            )
        path = reverse('authors')
        request = RequestFactory().get(path)
        response = AuthorListView.as_view()(request)
        response.render()
        assert response.status_code == 200

        assert 'is_paginated' in response.context_data
        assert 'is_paginated' in response.context_data
        assert response.context_data['is_paginated'] == True
        assert len(response.context_data['author_list']) == 10