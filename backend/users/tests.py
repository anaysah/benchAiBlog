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
        # python3 manage.py test users.tests.VerifyEmailViewTest.test_verify_email_missing_token
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Token is required")

    def test_verify_email_already_verified(self):
        # python3 manage.py test users.tests.VerifyEmailViewTest.test_verify_email_already_verified
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
        # python3 manage.py test users.tests.LoginViewTest.test_login_success_with_username
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
        # python3 manage.py test users.tests.LoginViewTest.test_login_invalid_credentials_with_username
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

from .models import CustomUser, OTP
from unittest.mock import patch

class ForgetPasswordViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123"
        )
        self.forget_password_url = reverse('forget_password')  # URL for forget password

    @patch('users.views.send_mail')  # Mock the send_mail function
    def test_forget_password_success(self, mock_send_mail):
        # python3 manage.py test users.tests.ForgetPasswordViewTest.test_forget_password_success
        # Test successful forget password request
        data = {"email": "testuser@example.com"}
        response = self.client.post(self.forget_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "OTP sent to your email")
        self.assertTrue(OTP.objects.filter(user=self.user).exists())  # Check if OTP is created
        mock_send_mail.assert_called_once()  # Ensure email was sent

    def test_forget_password_user_not_found(self):
        # python3 manage.py test users.tests.ForgetPasswordViewTest.test_forget_password_user_not_found
        # Test forget password request for a non-existent user
        data = {"email": "nonexistent@example.com"}
        response = self.client.post(self.forget_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "User with this email does not exist")

    def test_forget_password_invalid_email(self):
        # python3 manage.py test users.tests.ForgetPasswordViewTest.test_forget_password_invalid_email
        # Test forget password request with an invalid email format
        data = {"email": "invalid-email"}
        response = self.client.post(self.forget_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # Check for email validation error

    def test_forget_password_missing_email(self):
        # python3 manage.py test users.tests.ForgetPasswordViewTest.test_forget_password_missing_email
        # Test forget password request with missing email field
        data = {}
        response = self.client.post(self.forget_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # Check for missing email error

class VerifyOTPViewTest(APITestCase):
    # python3 manage.py test users.tests.VerifyOTPViewTest
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123"
        )
        self.otp = OTP.objects.create(user=self.user, otp="123456")
        self.verify_otp_url = reverse('verify_otp')  # URL for verify OTP

    def test_verify_otp_success(self):
        # python3 manage.py test users.tests.VerifyOTPViewTest.test_verify_otp_success
        # Test successful OTP verification
        data = {"email": "testuser@example.com", "otp": "123456"}
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "OTP verified successfully")

    def test_verify_otp_invalid_otp(self):
        # python3 manage.py test users.tests.VerifyOTPViewTest.test_verify_otp_invalid_otp
        # Test OTP verification with an invalid OTP
        data = {"email": "testuser@example.com", "otp": "999999"}
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid OTP or email")

    def test_verify_otp_invalid_email(self):
        # python3 manage.py test users.tests.VerifyOTPViewTest.test_verify_otp_invalid_email
        # Test OTP verification with an invalid email
        data = {"email": "invalid@example.com", "otp": "123456"}
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid OTP or email")

    def test_verify_otp_missing_fields(self):
        # python3 manage.py test users.tests.VerifyOTPViewTest.test_verify_otp_missing_fields
        # Test OTP verification with missing fields
        data = {}
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("otp", response.data)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, OTP

class ResetPasswordViewTest(APITestCase):
    # python3 manage.py test users.tests.ResetPasswordViewTest
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="strongpassword123"
        )
        # Create an OTP for the user
        self.otp = OTP.objects.create(user=self.user, otp="123456")
        self.reset_password_url = reverse('reset_password')  # URL for reset password

    def test_reset_password_success(self):
        # Test successful password reset
        data = {
            "email": "testuser@example.com",
            "otp": "123456",
            "new_password": "newstrongpassword123",
            "confirm_password": "newstrongpassword123"
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset successfully")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newstrongpassword123"))  # Verify password is updated

    def test_reset_password_invalid_otp(self):
        # Test password reset with an invalid OTP
        data = {
            "email": "testuser@example.com",
            "otp": "999999",
            "new_password": "newstrongpassword123",
            "confirm_password": "newstrongpassword123"
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid OTP or email")

    def test_reset_password_mismatched_passwords(self):
        # Test password reset with mismatched new_password and confirm_password
        data = {
            "email": "testuser@example.com",
            "otp": "123456",
            "new_password": "newstrongpassword123",
            "confirm_password": "differentpassword123"
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.data)  # Check for mismatched password error

    def test_reset_password_missing_fields(self):
        # Test password reset with missing fields
        data = {
            "email": "testuser@example.com",
            "otp": "123456",
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data)
        self.assertIn("confirm_password", response.data)

    def test_reset_password_invalid_email(self):
        # Test password reset with an invalid email
        data = {
            "email": "invalid@example.com",
            "otp": "123456",
            "new_password": "newstrongpassword123",
            "confirm_password": "newstrongpassword123"
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid OTP or email")