from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from http import HTTPStatus

from ..models import Group, Post


User = get_user_model()


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title="test group",
            slug="test_slug",
            description="Тестовое описание"
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Noname')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        '''Проверка создания поста'''
        posts_count = Post.objects.count()
        form_data = {'text': self.post.text,
                     'group': self.group.id}
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data, follow=True)
        error_name1 = 'Данные поста не совпадают'
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Post.objects.filter(
                        text=self.post.text, group=1,
                        author=self.user).exists(), error_name1)
        error_name2 = 'Поcт не добавлен в базу данных'
        self.assertEqual(Post.objects.count(),
                         posts_count + 1, error_name2)

    def test_not_create_post_guest_client(self):
        '''Проверка новый пост не создан при Post запросе
        неавторизованного пользователя'''
        posts_count = Post.objects.count()
        form_data = {'text': self.post.text,
                     'group': self.group.id}
        response = self.guest_client.post(reverse('posts:post_create'),
                                          data=form_data, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), posts_count)

    def test_create_post_without_group(self):
        '''Проверка создания поста без группы'''
        posts_count = Post.objects.count()
        form_data = {'text': self.post.text,
                     'group': ''}
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name = 'Поcт не добавлен в базу данных'
        self.assertEqual(Post.objects.count(),
                         posts_count + 1, error_name)

    def test_edit_post_not_accessed_for_guest_client(self):
        """Страница post_edit недоступна неавторизованному пользователю"""
        response = self.guest_client.get(
            'posts/<int:post_id>/edit/',
            follow=True)
        self.assertTrue(response.status_code, 301)
