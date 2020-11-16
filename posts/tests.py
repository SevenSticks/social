from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Group, Post

User = get_user_model()


class TestsMy(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'john'
        self.text = 'Test text'
        self.user = User.objects.create(
                        username=self.username,
                        email="connor@skynet.com",
                        password="12345"
                        )
        self.group = Group.objects.create(title="Tests group", slug="test")

    def postCreate(self) -> object:
        """ Post for tests """
        self.client.force_login(user=self.user)
        self.create_post = self.client.post(
            reverse('new_post'),
            {
                'text': self.text,
                'group': self.group.id
            })
        return self.create_post

    def reverseGetPage(self, url, **kwargs):
        post = self.client.get(reverse(url, kwargs=kwargs))
        return post

    def testPageCodes(self) -> None:
        self.assertNotEqual(self.client.get(reverse('index')), 200)
        self.assertNotEqual(self.client.get(reverse('admin:index')), 302)

    def testTemplates(self) -> None:
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def testProfilePage(self) -> None:
        response = self.client.get(reverse(
            'profile',
            kwargs={'username': self.username}
        ))
        self.assertEqual(response.status_code, 200)

    def testPostCreate(self) -> None:
        self.new_post = self.postCreate()
        self.get_post = Post.objects.filter(
            author__username=self.username,
            text=self.text,
            group_id=self.group.id
        )
        self.assertTrue(self.get_post)

    def testNotAuthorizedUser(self) -> None:
        response = self.client.get(reverse('new_post'), follow=True)
        post = Post.objects.filter(pk=1)
        self.assertFalse(post)
        self.assertRedirects(
            response,
            '/auth/login/?next=/new/',
            status_code=302
        )

    def testNewPost(self) -> None:
        self.new_post = self.postCreate()
        self.post = Post.objects.get(pk=1)

        self.check_index = self.reverseGetPage(
            'index',
        )
        self.assertContains(
            self.check_index, status_code=200, text=self.text
        )
        self.check_profile = self.reverseGetPage(
            'profile',
            username=self.user.username
        )
        self.assertContains(
            self.check_profile, status_code=200, text=self.text
        )
        self.check_post = self.reverseGetPage(
            'post',
            username=self.user.username,
            post_id=self.post.id
        )
        self.assertContains(
            self.check_post, status_code=200, text=self.text
        )

    def testPostEdit(self) -> None:
        self.new_post = self.postCreate()
        self.post = Post.objects.get(pk=1)
        self.new_text = 'New Test Text'

        """Group not defined to check post in old group"""
        self.update_post = self.client.post(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id
                },
            ),
            {
                'text': self.new_text,
            },
            follow=True
        )
        self.group_post = self.client.post(
            reverse('group_posts', kwargs={'slug': self.group.slug})
        )
        self.assertContains(self.update_post, self.new_text)
        self.assertNotContains(self.group_post, self.new_text)
