from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Explicitly allow unauthenticated access

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    "id": user.id,
                    "email": user.email,
                    "message": "User registered successfully"
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

