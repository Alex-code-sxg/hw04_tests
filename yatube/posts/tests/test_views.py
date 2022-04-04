from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Group, Post

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
                        kwargs={'post_id': f'{self.post.pk}'})
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_and_group_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        templates_context = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': f'{self.group.slug}'}),
            reverse('posts:profile', kwargs={'username':
                    f'{self.user.username}'})
        }
        for template_context in templates_context:
            with self.subTest(template_context=template_context):
                response = self.authorized_client.get(template_context)
                first_post = response.context['page_obj'][0]
                self.assertEqual(
                    first_post.text,
                    PostURLTest.post.text)
                self.assertEqual(
                    first_post.author.username,
                    PostURLTest.post.author.username)
                self.assertEqual(
                    first_post.group.title,
                    PostURLTest.post.group.title)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': f'{self.user.username}'}))
        first_post = response.context['page_obj'][0]
        self.assertEqual(
            first_post.text,
            PostURLTest.post.text)
        self.assertEqual(
            first_post.author.username,
            PostURLTest.post.author.username)
        self.assertEqual(
            first_post.group.title,
            PostURLTest.post.group.title)
