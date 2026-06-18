from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnswerViewSet, QuestionViewSet

router = DefaultRouter()
# Router는 ViewSet의 CRUD URL을 자동으로 만들어준다.
router.register('questions', QuestionViewSet, basename='question')
router.register('answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
    # 질문 하위 답변 생성 endpoint를 별도로 제공해 URL 의미를 명확히 한다.
    path('questions/<int:question_id>/answers/', AnswerViewSet.as_view({'post': 'create'}), name='question-answer-create'),
]
