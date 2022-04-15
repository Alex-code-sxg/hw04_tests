from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from yatube.settings import AMOUNT_CHAR

from ..models import Group, Post

settings.DEBUG = True


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_models_have_correct_post_name(self):
        """Проверяем, что у модели Post выводятся 15 символов поста"""
        post = PostModelTest.post
        check = post.text[:AMOUNT_CHAR]
        self.assertEqual(check, str(post))

    def test_verbose_name(self):
        """verbose_name в модели Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Название группы',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в модели Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_helps = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_helps.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_verbose_name(self):
        """verbose_name в модели Group совпадает с ожидаемым."""
        post = GroupModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Адрес ссылки',
            'description': 'Описание',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)
