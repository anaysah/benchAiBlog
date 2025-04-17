from django.urls import path
from django.http import JsonResponse


urlpatterns = [
    path('hello-blog/', lambda request: JsonResponse({'message': 'Hello, Blogs! Blogs api are working'}), name='hello_blog'),
]