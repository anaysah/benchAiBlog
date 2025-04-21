from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile

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
