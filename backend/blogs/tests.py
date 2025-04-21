from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Comment

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile

from rest_framework.test import APIClient
from rest_framework import status
from .models import Post


def generate_test_image():
    # Create an in-memory image
    image = Image.new('RGB', (100, 100), color='red')
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(temp_file, format='JPEG')
    temp_file.seek(0)
    return SimpleUploadedFile('test.jpg', temp_file.read(), content_type='image/jpeg')


# Create your tests here.
class CategoryViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('category-list')
        self.category = {
            "name": "Test Category",
            # "slug": "test-category",
            "icon_svg": "<svg></svg>"
        }
        # create a admin
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123",
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_category(self):
        response = self.client.post(self.url, self.category)
        print(response)
        print(response.data)  # This will show any validation errors returned by DRF

        print("ursl is this", self.url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.category['name'])
        # self.assertEqual(response.data['slug'], self.category['slug'])
        self.assertEqual(response.data['icon_svg'], self.category['icon_svg'])

    def test_get_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category['name'])
        self.assertEqual(response.data[0]['icon_svg'], self.category['icon_svg'])

class PostViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('post-list')
        self.category = Category.objects.create(name="Test Category")
        self.post = {
            "title": "Test Post",
            "snippet": "Test Snippet",
            "body": "Test Body Content lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
            "status": "published",
            "category_id": self.category.id
        }

        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123",
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_post(self):
        response = self.client.post(self.url, self.post)
        # print(response)
        # print(response.data)
        self.assertEqual(response.status_code, 201)

    def test_create_post_with_invalid_category(self):
        invalid_post = {
            "title": "Invalid Post",
            "snippet": "Invalid Snippet",
            "body": "Invalid Body Content",
            "status": "published",
            "category_id": 999  # Invalid category ID
        }
        response = self.client.post(self.url, invalid_post)
        self.assertEqual(response.status_code, 400)

    def test_create_post_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, self.post)
        self.assertEqual(response.status_code, 401)
    
    def test_create_post_with_thumbnail(self):
        image = generate_test_image()
        post_data = {
            "title": "Post with Image",
            "snippet": "Image test",
            "body": "Body here... lorem ipsum dolor sit amet lorem ipsum 100 times lorem ipsum dolor sit amet  lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet", 
            "category_id": self.category.id,
            "thumbnail": image
        }
        response = self.client.post(self.url, post_data, format='multipart')
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('thumbnail', response.data)

class CommentViewSetTest(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = CustomUser.objects.create_user(email="user1@example.com", password="pass1234")
        self.user2 = CustomUser.objects.create_user(email="user2@example.com", password="pass1234")
        self.user3 = CustomUser.objects.create_user(email="user3@example.com", password="pass1234")

        # Create authenticated clients
        self.client1 = self.get_authenticated_client(self.user1)
        self.client2 = self.get_authenticated_client(self.user2)
        self.client3 = self.get_authenticated_client(self.user3)

        self.category = Category.objects.create(name="Test Category")
        self.post_data = {
            "title": "Test Post",
            "snippet": "Test Snippet",
            "body": "Test Body Content lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
            "status": "published",
            "category": self.category,
            "author": self.user1
        }
        self.post = Post.objects.create(**self.post_data)
        self.other_post = Post.objects.create(**self.post_data)
        self.other_post.author = self.user2
        self.other_post.save()

        self.url = reverse('comment-list')

    def get_authenticated_client(self, user):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    def test_create_root_comment(self):
        data = {
            "post": self.post.id,
            "content": "This is a root comment."
        }
        response = self.client1.post(self.url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['parent'])

    def test_create_reply_comment(self):
        root_comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content="Root comment"
        )

        data = {
            "post": self.post.id,
            "parent": root_comment.id,
            "content": "This is a reply."
        }
        response = self.client2.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['parent'], root_comment.id)

    def test_create_invalid_reply_different_post(self):
        # other_post = Post.objects.create(
        #     author=self.user1,
        #     title="Another Post",
        #     slug="another-post",
        #     content="Another post content"
        # )

        root_comment = Comment.objects.create(
            post=self.other_post,
            author=self.user1,
            content="Wrong post"
        )

        data = {
            "post": self.post.id,
            "parent": root_comment.id,
            "content": "Invalid reply"
        }
        response = self.client1.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_comment_by_owner(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content="Original content"
        )

        url = reverse('comment-detail', args=[comment.id])
        response = self.client1.patch(url, {"content": "Updated content"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated content")

    def test_update_comment_by_other_user_forbidden(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content="Someone else's comment"
        )

        url = reverse('comment-detail', args=[comment.id])
        response = self.client2.patch(url, {"content": "Hacked!"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_comment_soft(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content="To be deleted"
        )

        url = reverse('comment-detail', args=[comment.id])
        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        comment.refresh_from_db()
        self.assertTrue(comment.is_deleted)