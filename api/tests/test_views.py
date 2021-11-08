from django.test import TestCase
from django.urls import resolve
from ..views import home


class HomePageViewTestCase(TestCase):
    def test_home_page_resolve_to_correct_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_part_page_return_correct_html(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/index.html')
