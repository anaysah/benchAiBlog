from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category

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
        category = Category.objects.create(name="Test Category")
        self.post = {
            "title": "Test Post",
            "snippet": "Test Snippet",
            "body": "Test Body Content lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet",
            "status": "published",
            "category_id": category.id
        }

        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123",
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_post(self):
        response = self.client.post(self.url, self.post)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, 201)