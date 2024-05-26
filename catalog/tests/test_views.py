from django.test import TestCase
from django.urls import reverse

from catalog.models import Author
from django.contrib.auth.models import User

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')

        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Dominique {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('catalog:authors'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # user log in
        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('catalog:authors'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        # user log in
        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('catalog:authors'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        # user log in
        self.client.login(username='testuser', password='12345')

        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('catalog:authors')+'?page=2', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)
