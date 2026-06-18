from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Answer, Question


class QnaApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='testpass123')
        self.other = User.objects.create_user(username='user2', password='testpass123')
        self.question = Question.objects.create(author=self.user, subject='DRF 질문', content='Serializer가 무엇인가요?')

    def authenticate(self, user):
        # API 테스트에서는 force_authenticate로 JWT 발급 과정을 생략하고 인증 상태를 만들 수 있다.
        self.client.force_authenticate(user=user)

    def test_question_list_is_public(self):
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_can_create_question(self):
        self.authenticate(self.user)
        response = self.client.post('/api/questions/', {
            'subject': 'JWT 질문',
            'content': 'JWT는 어디에 담아서 보내나요?',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_anonymous_user_cannot_create_question(self):
        response = self.client.post('/api/questions/', {
            'subject': '비로그인 질문',
            'content': '작성 가능한가요?',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_can_update_question(self):
        self.authenticate(self.user)
        response = self.client.patch(f'/api/questions/{self.question.id}/', {
            'subject': '수정된 제목',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.subject, '수정된 제목')

    def test_other_user_cannot_update_question(self):
        self.authenticate(self.other)
        response = self.client.patch(f'/api/questions/{self.question.id}/', {
            'subject': '권한 없는 수정',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_answer_create_under_question(self):
        self.authenticate(self.other)
        response = self.client.post(f'/api/questions/{self.question.id}/answers/', {
            'content': 'Serializer는 JSON 변환과 검증을 담당합니다.',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)

    def test_author_cannot_vote_own_question(self):
        self.authenticate(self.user)
        response = self.client.post(f'/api/questions/{self.question.id}/vote/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
