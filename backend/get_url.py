# This file is a standalone script to generate a full URL from a Django URL name.

# How to use it?
# python get_url.py <url_name>
# python3 get_url.py <url_name>


# save this as get_url.py in your Django project root
from django.conf import settings
from django.urls import reverse
import os
import sys
from decouple import config


# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

def get_full_url(url_name):
    try:
        full_url = reverse(url_name)
        print(full_url)
        domain = config('DOMAIN')
        return f"{domain}{full_url}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_url.py <url_name>")
    else:
        url_name = sys.argv[1]
        result = get_full_url(url_name)
        print(result)