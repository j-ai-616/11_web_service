from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AccountApiTests(APITestCase):
    def test_register(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'password': 'testpass123',
            'email': 'newuser@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertNotIn('password', response.data)

    def test_jwt_login(self):
        # JWT 로그인 API는 username/password를 받아 access/refresh token을 반환한다.
        User.objects.create_user(username='user1', password='testpass123')
        response = self.client.post('/api/auth/token/', {
            'username': 'user1',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_me_requires_authentication(self):
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
