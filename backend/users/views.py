from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import EmailVerificationToken


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