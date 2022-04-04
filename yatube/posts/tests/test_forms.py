from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Group, Post
from ..forms import PostForm

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
        cls.form = PostForm()

    def setUp(self):
        self.user = User.objects.create_user(username='Noname')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
    
    def test_create_post(self):
        '''Проверка создания поста'''
        posts_count = Post.objects.count()
        form_data = {'text': 'Текст записанный в форму',
                     'group': self.group.id}
        response = self.authorized_client.post(reverse('posts:post_create'),
                        data=form_data, follow=True)
        error_name1 = 'Данные поста не совпадают'
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(
                text='Текст записанный в форму', group=1,
                        author=self.user).exists(), error_name1)
        error_name2 = 'Поcт не добавлен в базу данных'
        self.assertEqual(Post.objects.count(),
                         posts_count + 1, error_name2)
                         