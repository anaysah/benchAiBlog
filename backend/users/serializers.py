# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser
from .models import EmailVerificationToken
import uuid
from decouple import config
from django.urls import reverse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'confirm_password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        token = str(uuid.uuid4())
        EmailVerificationToken.objects.create(user=user, token=token)
        self.send_verification_email(user, token)
        return user
    
    def send_verification_email(self, user, token):
        from django.core.mail import send_mail
        verify_url = reverse('verify_email') 
        verification_url = f"{verify_url}?token={token}"

        verification_link = f"{config('DOMAIN')}{verification_url}"
        print("tokenurl: ", verification_link)

        subject = 'Verify your email address'
        message = f'Please click this link to verify your email: {verification_link}'
        from_email = config('DEFAULT_FROM_EMAIL')
        recipient_list = [user.email]
        
        # send_mail(subject, message, from_email, recipient_list)
        # print(subject, message, from_email, recipient_list)