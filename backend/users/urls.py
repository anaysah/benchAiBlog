from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from .views import RegisterView
from django.http import JsonResponse
from .views import VerifyEmailView

from .views import ForgetPasswordView
from .views import VerifyOTPView
from .views import ResetPasswordView


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # login
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),  
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),

    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    path('hello/', lambda request: JsonResponse({'message': 'Hello, world!'}), name='hello_world'),
]
