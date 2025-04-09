from django.test import TestCase
from django.urls import reverse

class HelloApiTest(TestCase):
    def test_hello_api(self):
        url = reverse('hello_world')  # Ensure the URL name matches your configuration
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, world!"})

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class RegisterViewTest(APITestCase):
    def test_register_user_success(self):
        url = reverse('register')  # Ensure the URL name matches your configuration
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123"  # Include this if your serializer requires it
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(response.data["message"], "User registered successfully")
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_register_user_invalid_data(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "short",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_register_user_missing_fields(self):
        url = reverse('register')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

class LoginViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123"
        )
        self.login_url = reverse('token_obtain_pair')  # URL for obtaining tokens

    def test_login_success_with_username(self):
        # Test successful login using username
        data = {
            "username": "testuser",
            "password": "strongpassword123"
        }
        response = self.client.post(self.login_url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Check if access token is returned
        self.assertIn("refresh", response.data)  # Check if refresh token is returned

    def test_login_invalid_credentials_with_username(self):
        # Test login with invalid credentials using username
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)  # Check for error message

    def test_login_nonexistent_user_with_username(self):
        # Test login with a non-existent user using username
        data = {
            "username": "nonexistentuser",
            "password": "somepassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)  # Check for error message

    def test_login_missing_fields_with_username(self):
        # Test login with missing fields using username
        data = {
            "username": "testuser"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  # Check for missing password error