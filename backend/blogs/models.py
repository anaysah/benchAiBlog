from django.db import models
from django.urls import reverse
from django.conf import settings
from users.models import CustomUser
import os
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
import bleach
from django.utils.text import slugify
import string
import random

def random_suffix(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def validate_image_extension(value):
    """Ensure uploaded images have valid extensions."""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension. Allowed: JPG, JPEG, PNG, GIF")

def get_image_filename(instance, filename):
    """Generate a path for uploaded images based on the instance ID."""
    id = instance.id or 0  # Fallback to 0 if ID is None
    return os.path.join('images', str(id), filename)

def validate_image_size(value):
    """Ensure uploaded images are under 5MB."""
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError("Image file too large (max 5MB).")
    
def validate_svg_content(value):
    """Ensure the input is valid SVG content."""
    if not value.strip().startswith('<svg'):
        raise ValidationError("Content must be valid SVG starting with <svg> tag.")
    if not value.strip().endswith('</svg>'):
        raise ValidationError("Content must be valid SVG ending with </svg> tag.")

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon_svg = models.TextField(
        validators=[validate_svg_content],
        help_text="Enter valid SVG code (e.g., <svg>...</svg>).",
        blank=True, null=True
    )

    def save(self, *args, **kwargs):
        """Auto-generate slug and sanitize SVG content before saving."""
        if not self.slug:
            self.slug = slugify(self.name)
        if self.icon_svg:
            # Sanitize SVG to remove harmful elements
            allowed_tags = [
                'svg', 'path', 'g', 'circle', 'rect', 'line', 'polyline', 'polygon',
                'ellipse', 'text', 'clipPath', 'defs', 'use'
            ]
            allowed_attrs = {
                'svg': [
                    'viewBox', 'width', 'height', 'xmlns', 'fill', 'stroke', 'stroke-width',
                    'stroke-linecap', 'stroke-linejoin', 'class', 'transform', 'opacity', 'style'
                ],
                'circle': ['cx', 'cy', 'r', 'fill', 'stroke', 'stroke-width', 'transform', 'opacity'],
                'use': ['xlink:href', 'x', 'y', 'transform'],
                '*': [
                    'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'd',
                    'class', 'transform', 'x', 'y', 'rx', 'ry', 'points', 'opacity', 'id', 'style'
                ]
            }
            self.icon_svg = bleach.clean(
                self.icon_svg,
                tags=allowed_tags,
                attributes=allowed_attrs,
                strip=True
            )
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('home')
    
    def get_absolute_url(self):
        return reverse('category_detail', args=(self.name,))

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']  # Order categories alphabetically by default

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        related_name='posts'
    )
    thumbnail = models.ImageField(
        upload_to=get_image_filename,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size]
    )
    # thumbnail_url = models.URLField(
    #     blank=True,
    #     validators=[
    #         RegexValidator(
    #             regex=r'\.(jpg|jpeg|png|gif)$',
    #             message="URL must point to a valid image (JPG, JPEG, PNG, or GIF)."
    #         )
    #     ]
    # )
    snippet = models.CharField(max_length=255)
    body = body = models.TextField(
        validators=[MinLengthValidator(50, "Post body must be at least 50 characters long.")],
        blank=False
    )
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    # search_vector = SearchVectorField(null=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Sanitize body content before saving."""
        if not self.slug:
            while True:
                base_slug = slugify(self.title)
                suffix = random_suffix()
                new_slug = f"{base_slug}-{suffix}"
                if not Post.objects.filter(slug=new_slug).exists():
                    self.slug = new_slug
                    break
        if self.body:
            self.body = bleach.clean(self.body, tags=['p', 'b', 'i', 'a'], attributes={'a': ['href']})
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} | {self.author}"

    def get_absolute_url(self):
        return reverse('blogPage', args=(self.slug,))

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['date']),
            models.Index(fields=['category']),
            # GinIndex(fields=['search_vector']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_post_slug')
        ]

class Comment(models.Model):
    """A model representing a comment on a blog post, supporting nested replies."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField(
        validators=[MinLengthValidator(10, "Comment must be at least 10 characters long.")],
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Sanitize comment content before saving."""
        if self.content:
            self.content = bleach.clean(
                self.content,
                tags=['p', 'b', 'i', 'a'],
                attributes={'a': ['href']}
            )
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.post}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['parent']),
            models.Index(fields=['created_at']),
        ]