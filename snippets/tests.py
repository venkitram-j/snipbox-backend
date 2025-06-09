from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .models import Snippet, Tag

class JWTAuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_successful_token_generation(self):
        url = reverse('token-obtain-pair')  # Replace with your token generation URL
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials(self):
        url = reverse('token-obtain-pair')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_valid_token(self):
        token = str(AccessToken.for_user(self.user))
        url = reverse('snippets-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_without_token(self):
        url = reverse('snippets-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class SnippetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = self.get_access_token()
    
    def get_access_token(self):
        token = AccessToken.for_user(self.user)
        return str(token)

    def test_snippet_model_viewset(self):
        data = {"title": "Test", "note": "Test snippet", "tags": ["test-tag", "another-test-tag"]}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # test create
        response = self.client.post(reverse("snippets-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)
        
        # test overview
        response = self.client.get(reverse("snippets-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data.get("data")), 1)

        # test retrieve
        instance = Snippet.objects.filter().first()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(reverse("snippets-detail", kwargs={"pk": instance.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["note"], "Test snippet")

        # test update
        updated_data = {"title": "Test", "note": "Test snippet updated", "tags": ["test-tag", "another-test-tag"]}
        response = self.client.put(reverse("snippets-detail", kwargs={"pk": instance.pk}), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instance = Snippet.objects.filter().first()
        self.assertEqual(instance.note, "Test snippet updated")

        # test delete
        response = self.client.delete(reverse("snippets-detail", kwargs={"pk": instance.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Snippet.objects.count(), 0)
