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
from .models import CustomUser


class RegisterViewTest(APITestCase):
    def test_register_user_success(self):
        url = reverse('register')  # Ensure the URL name matches your configuration
        data = {
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123"  # Include this if your serializer requires it
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], data["email"])
        # self.assertEqual(response.data["message"], "User registered successfully")
        self.assertTrue(CustomUser.objects.filter(email=data["email"]).exists())

    def test_register_user_invalid_data(self):
        url = reverse('register')
        data = {
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

from .models import EmailVerificationToken

class VerifyEmailViewTest(APITestCase):
    # python3 manage.py test users.tests.VerifyEmailViewTest
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123"
        )
        self.verify_url = reverse('verify_email')  # URL for verifying email
        self.token = EmailVerificationToken.objects.create(
            user=self.user,
            token="testtoken"
        )

    def test_verify_email_success(self):
        # python3 manage.py test users.tests.VerifyEmailViewTest.test_verify_email_success
        url = f"{self.verify_url}?token={self.token.token}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Email successfully verified")
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.assertFalse(EmailVerificationToken.objects.filter(token=self.token.token).exists())

    def test_verify_email_invalid_token(self):
        # python3 manage.py test users.tests.VerifyEmailViewTest.test_verify_email_invalid_token
        url = f"{self.verify_url}?token=invalidtoken"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid or expired token")

    def test_verify_email_missing_token(self):
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Token is required")

    def test_verify_email_already_verified(self):
        self.user.is_verified = True
        self.user.save()
        url = f"{self.verify_url}?token={self.token.token}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Email already verified")
        


class LoginViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123"
        )
        self.login_url = reverse('token_obtain_pair')  # URL for obtaining tokens

    def test_login_success_with_username(self):
        # Test successful login using username
        data = {
            "email":"testuser@example.com",
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
            "email":"testuser@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)  # Check for error message

    def test_login_nonexistent_user_with_username(self):
        # Test login with a non-existent user using username
        data = {
            "email":"testuser@example.com",
            "password": "somepassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)  # Check for error message

    def test_login_missing_fields_with_username(self):
        # Test login with missing fields using username
        data = {
            "email":"testuser@example.com",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  # Check for missing password error