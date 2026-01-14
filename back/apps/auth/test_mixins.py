from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticatedTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        
        # Get JWT token
        response = self.client.post('/auth/jwt/create/', {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
