from django.test import TestCase, Client
from http import HTTPStatus


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/author/."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_url_uses_correct_template(self):
        """Проверка шаблона для адреса АВТОР."""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/author.html')

    def test_tech_url_uses_correct_template(self):
        """Проверка шаблона для адреса ТЕХНОЛОГИИ."""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')
