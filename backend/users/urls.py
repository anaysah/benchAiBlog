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
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # login
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh
    path('api/auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),  
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify_email'),

    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    path('api/hello/', lambda request: JsonResponse({'message': 'Hello, world!'}), name='hello_world'),
]
