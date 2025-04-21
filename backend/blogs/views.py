from django.shortcuts import render
from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from backend.permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

class PostViewSet(viewsets.ModelViewSet):
    """API endpoint for posts."""
    queryset = Post.objects.filter(is_deleted=False, status='published')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['title', 'snippet', 'body']
    ordering_fields = ['date', 'title']
    ordering = ['-date']

    def perform_create(self, serializer):
        """Ensure only authenticated users can create posts."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Ensure only the author can update posts."""
        if self.get_object().author != self.request.user:
            raise serializers.ValidationError("You can only update your own posts.")
        serializer.save()

    def perform_destroy(self, serializer):
        """Soft delete posts instead of hard delete."""
        post = self.get_object()
        if post.author != self.request.user:
            raise serializers.ValidationError("You can only delete your own posts.")
        post.is_deleted = True
        post.save()


class CommentViewSet(viewsets.ModelViewSet):
    """API endpoint for comments."""
    queryset = Comment.objects.filter(is_deleted=False, is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post', 'parent']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        """Ensure only authenticated users can create comments."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Ensure only the author can update comments."""
        if self.get_object().author != self.request.user:
            raise serializers.ValidationError("You can only update your own comments.")
        serializer.save()

    def perform_destroy(self, serializer):
        """Soft delete comments instead of hard delete."""
        comment = self.get_object()
        if comment.author != self.request.user:
            raise serializers.ValidationError("You can only delete your own comments.")
        comment.is_deleted = True
        comment.save()