from django.test import TestCase
from django.urls import reverse

class HelloApiTest(TestCase):
    def test_hello_api(self):
        url = reverse('hello_world')  # Ensure the URL name matches your configuration
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, world!"})