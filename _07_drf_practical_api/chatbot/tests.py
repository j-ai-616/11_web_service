from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ChatMessage, ChatSession


class ChatbotApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='testpass123')
        self.other = User.objects.create_user(username='user2', password='testpass123')
        self.session = ChatSession.objects.create(user=self.user, title='DRF 상담')

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_user_can_create_chat_session(self):
        self.authenticate(self.user)
        response = self.client.post('/api/chat/sessions/', {'title': '새 상담'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatSession.objects.filter(user=self.user).count(), 2)

    def test_user_can_only_see_own_sessions(self):
        ChatSession.objects.create(user=self.other, title='다른 사용자 상담')
        self.authenticate(self.user)
        response = self.client.get('/api/chat/sessions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_other_user_cannot_read_session_messages(self):
        self.authenticate(self.other)
        response = self.client.get(f'/api/chat/sessions/{self.session.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_message_creates_human_and_ai_messages(self):
        self.authenticate(self.user)
        response = self.client.post(f'/api/chat/sessions/{self.session.id}/send/', {
            'content': 'DRF ViewSet이 뭐야?',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message_type'], 'ai')
        self.assertEqual(ChatMessage.objects.filter(session=self.session).count(), 2)
