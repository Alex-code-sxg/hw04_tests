from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

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
        check = post.text[:15]
        self.assertEqual(check, str(post))

    def test_verbose_name(self):
        """verbose_name в поле group совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'group': 'Название группы'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)
