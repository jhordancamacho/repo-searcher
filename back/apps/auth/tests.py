from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class RegisterAPITest(APITestCase):
    def test_register_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_duplicate_user(self):
        """
        Ensure we cannot create a user with a username that already exists.
        """
        # Create a user first
        User.objects.create_user(username='testuser', email='test@example.com', password='password')

        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser2@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginAPITest(APITestCase):
    def setUp(self):
        self.email = 'testuser@example.com'
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login_user(self):
        """
        Ensure a registered user can login.
        """
        url = reverse('login')
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)

    def test_login_invalid_credentials(self):
        """
        Ensure a user cannot login with invalid credentials.
        """
        url = reverse('login')
        data = {
            'email': self.email,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        """
        Ensure a nonexistent user cannot login.
        """
        url = reverse('login')
        data = {
            'email': 'nonexistentuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
