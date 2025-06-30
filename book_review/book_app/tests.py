from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, Review
from django.core.cache import cache

class BookAppTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title="Test Book", author="Test Author")

    def test_home_page_displays_books(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book") 

    def test_add_book(self):
        response = self.client.post(reverse('add_book'), {
            'title': 'Another Book',
            'author': 'Another Author'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Book.objects.filter(title="Another Book").exists())

    def test_cache_miss_path(self):
        cache.delete('books_list')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test Book")
