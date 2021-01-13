from django.db.models import Max
from django.test import Client, TestCase

from .models import User, Post, Follow, Like

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):

        # Create users
        user1 = User.objects.create(username="foo", email="foo@example.com", password="1234")
        user2 = User.objects.create(username="bar", email="bar@example.com", password="soon1234")
        user3 = User.objects.create(username="baz", email="baz@example.com", password="Soon1234")

        # Create posts
        post1 = Post.objects.create(content="This is a test case 1", poster=user1)
        post2 = Post.objects.create(content="This is a test case 2", poster=user2)
        post3 = Post.objects.create(content="This is a test case 3", poster=user3)
        post4 = Post.objects.create(content="This is a test case 4", poster=user2)


    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 3)

    def test_post_count(self):
        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 4)

    def test_invalid_password_1(self):
        user = User.objects.get(username="foo")
        self.assertFalse(user.is_password_valid())

    def test_invalid_password_2(self):
        user = User.objects.get(username="bar")
        self.assertFalse(user.is_password_valid())

    def test_valid_password(self):
        user = User.objects.get(username="baz")
        self.assertTrue(user.is_password_valid())

    def test_increase_likes(self):
        user = User.objects.get(username="foo")
        post = Post.objects.get(poster=user)

        for i in range(3):
            post.increase_likes()

        self.assertEqual(post.num_of_likes, 3)

    def test_decrease_likes(self):
        user = User.objects.get(username="baz")
        post = Post.objects.get(poster=user)
        post.num_of_likes = 3

        for i in range(3):
            post.decrease_likes()

        self.assertEqual(post.num_of_likes, 0)

    def test_user_posts_1(self):
        user = User.objects.get(username="bar")
        num_of_posts = Post.objects.filter(poster=user).count()
        self.assertEqual(num_of_posts, 2)

    def test_user_posts_2(self):
        user = User.objects.get(username="foo")
        num_of_posts = Post.objects.filter(poster=user).count()
        self.assertEqual(num_of_posts, 1)

    def test_index_page(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_object"].count(), 4)

    def test_valid_profile_page(self):
        user = User.objects.get(username="foo")
        posts = Post.objects.filter(poster=user.id)

        c = Client()
        response = c.get(f"/profile/{user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 1)

    def test_invalid_profile_page(self):
        max_id = User.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/profile/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
