from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from yatube.settings import AMOUNT_POSTS, PAG_TEST_AMOUNT

from ..models import Group, Post

settings.DEBUG = True


User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='newname')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(PostURLTest.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': (
                reverse('posts:group_list',
                        kwargs={'slug': f'{self.group.slug}'})
            ),
            'posts/profile.html': (
                reverse('posts:profile',
                        kwargs={'username': f'{self.user.username}'})
            ),
            'posts/post_detail.html': (
                reverse('posts:post_detail',
                        kwargs={'post_id': f'{self.post.pk}'})
            ),
            'posts/create_post.html': reverse('posts:post_create'),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_uses_author_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'posts/create_post.html': (
                reverse('posts:post_edit',
                        kwargs={'post_id': self.post.pk})
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_and_group_page_show_correct_context(self):
        """Шаблоны сформированы с правильным контекстом."""
        templates_context = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username':
                    self.user.username})
        }
        for template_context in templates_context:
            with self.subTest(template_context=template_context):
                response = self.authorized_client.get(template_context)
                first_post = response.context['page_obj'][0]
                self.assertEqual(
                    first_post.text,
                    PostURLTest.post.text)
                self.assertEqual(
                    first_post.author,
                    PostURLTest.post.author)
                self.assertEqual(
                    first_post.group,
                    PostURLTest.post.group)

    def test_profile_page_show_correct_context_author(self):
        """Шаблон profile сформирован с правильным контекстом (для автора)."""
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': self.user.username}))
        response.context['author']
        self.assertEqual(
            PostURLTest.user.username,
            PostURLTest.post.author.username)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='newname')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        cls.posts = []
        for i in range(0, PAG_TEST_AMOUNT):
            cls.posts.append(Post.objects.create(
                text=f'Рандомный текст{i}',
                author=cls.user,
                group=cls.group,
            ))

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_contains_ten_records(self):
        """Проверка паджинатора 10 постов страница 1."""
        pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test'}),
            reverse('posts:profile',
                    kwargs={'username': PaginatorViewsTest.user.username}
                    )
        ]
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(len(
                    response.context.get('page_obj')), AMOUNT_POSTS)

    def test_last_page_contains_three_records(self):
        """Проверка паджинатора 3 поста страница 2."""
        pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test'}),
            reverse('posts:profile',
                    kwargs={'username': PaginatorViewsTest.user.username}
                    )
        ]
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page + '?page=2')
                self.assertEqual(len(response.context.get(
                    'page_obj')), PAG_TEST_AMOUNT - AMOUNT_POSTS)
