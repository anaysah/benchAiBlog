from rest_framework import serializers
from .models import Category
from .models import Post, Comment
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon_svg']
        extra_kwargs = {
            'slug': {'required': False}  # Make slug field optional during serialization
        }

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model with nested replies."""
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'parent', 'content', 'created_at', 'updated_at', 'is_approved', 'is_deleted', 'replies']
        read_only_fields = ['author', 'created_at', 'updated_at', 'is_approved']
        extra_kwargs = {
            'parent': {'required': False}  # Make parent field optional during serialization
        }

    def get_replies(self, obj):
        """Recursively serialize replies."""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True, is_deleted=False), many=True).data
        return []

    def validate(self, data):
        """Ensure parent comment belongs to the same post."""
        if data.get('parent'):
            if data['parent'].post != data['post']:
                raise serializers.ValidationError("Parent comment must belong to the same post.")
        return data

    def create(self, validated_data):
        """Set the author to the authenticated user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model with comments."""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'author', 'category', 'thumbnail', 'category_id', 
            'snippet', 'body', 'slug', 'date', 'updated_at', 'status', 'is_deleted', 'comments'
        ]
        extra_kwargs = {
            'slug': {'required': False},  # Make slug field optional during serialization
            'status': {'required': False},  # Make status field optional during
            'is_deleted': {'required': False},  # Make is_deleted field optional during serialization
            # 'category': {'required': False}  # Make category field optional during serialization'
        }

        read_only_fields = ['author', 'date', 'updated_at', 'comments']