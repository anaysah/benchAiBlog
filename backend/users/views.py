from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import EmailVerificationToken
from .models import CustomUser
import uuid


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
            user = verification_token.user
            
            if user.is_verified:
                return Response({'message': 'Email already verified'}, 
                              status=status.HTTP_400_BAD_REQUEST)
                
            user.is_verified = True
            user.save()
            verification_token.delete()
            
            return Response({'message': 'Email successfully verified'}, 
                          status=status.HTTP_200_OK)
            
        except EmailVerificationToken.DoesNotExist:
            return Response({'error': 'Invalid or expired token'}, 
                          status=status.HTTP_400_BAD_REQUEST)

from django.core.mail import send_mail
from .serializers import ForgetPasswordSerializer
from .models import OTP
from .utils import generate_otp


# forget password api
class ForgetPasswordView(APIView):
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                # Generate 6-digit OTP
                otp = generate_otp()
                
                # Save OTP
                OTP.objects.create(user=user, otp=otp)
                
                # Send OTP via email
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, 
                              status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from datetime import timedelta
from django.utils import timezone
from .serializers import OTPVerificationSerializer


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                user = CustomUser.objects.get(email=email)
                otp_obj = OTP.objects.filter(
                    user=user,
                    otp=otp,
                    created_at__gte=timezone.now() - timedelta(minutes=15)  # 15-minute validity
                ).latest('created_at')
                
                return Response({"message": "OTP verified successfully"}, 
                              status=status.HTTP_200_OK)
            except (CustomUser.DoesNotExist, OTP.DoesNotExist):
                return Response({"error": "Invalid OTP or email"}, 
                              status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from .serializers import ResetPasswordSerializer

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']
            
            if new_password != confirm_password:
                return Response({"confirm_password": ["Passwords do not match"]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = CustomUser.objects.get(email=email)
                otp_obj = OTP.objects.filter(
                    user=user,
                    otp=otp,
                    created_at__gte=timezone.now() - timedelta(minutes=15)
                ).latest('created_at')

                                  
                
                # Update password and mark OTP as used
                user.set_password(new_password)
                user.save()
                otp_obj.save()

                # delete the otp
                otp_obj.delete()
                
                return Response({"message": "Password reset successfully"}, 
                              status=status.HTTP_200_OK)
            except (CustomUser.DoesNotExist, OTP.DoesNotExist):
                return Response({"error": "Invalid OTP or email"}, 
                              status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)