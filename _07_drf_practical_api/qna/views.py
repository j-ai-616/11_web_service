from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Answer, Question
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    AnswerSerializer,
    QuestionCreateUpdateSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):
    # ModelViewSet은 list/retrieve/create/update/partial_update/destroy를 기본 제공한다.
    # 즉, 별도 메서드를 전부 만들지 않아도 질문 CRUD API가 자동으로 구성된다.
    queryset = Question.objects.select_related('author').prefetch_related('answers', 'voters').all()

    # 조회는 비로그인도 가능하지만, 생성/수정/삭제는 인증과 작성자 권한을 검사한다.
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # SearchFilter는 ?search=검색어, OrderingFilter는 ?ordering=필드명 요청을 처리한다.
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject', 'content', 'author__username']
    ordering_fields = ['created_at', 'modified_at']

    def get_serializer_class(self):
        # 같은 Question 모델이라도 API 목적에 따라 serializer를 다르게 사용한다.
        # 목록은 가볍게, 상세는 답변까지 포함, 생성/수정은 입력 필드 중심으로 분리한다.
        if self.action == 'list':
            return QuestionListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionCreateUpdateSerializer
        return QuestionDetailSerializer

    def perform_create(self, serializer):
        # 클라이언트가 author 값을 보내지 않아도 현재 로그인 사용자를 작성자로 저장한다.
        # 작성자 위조를 막기 위해 author는 요청 데이터가 아니라 request.user에서 가져온다.
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        # @action(detail=True)은 /api/questions/{id}/vote/ 같은 개별 객체용 추가 API를 만든다.
        # 기본 CRUD에 없는 "추천/추천취소" 같은 기능을 ViewSet 안에 확장할 때 사용한다.
        question = self.get_object()

        # 본인 글 추천을 막아 추천 수 조작을 방지한다.
        if question.author_id == request.user.id:
            return Response({'detail': '본인이 작성한 질문은 추천할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 이미 추천한 사용자면 추천 취소, 처음 추천하는 사용자면 추천 추가로 동작한다.
        # ManyToManyField의 add/remove를 사용해 voters 목록을 갱신한다.
        if question.voters.filter(id=request.user.id).exists():
            question.voters.remove(request.user)
            voted = False
        else:
            question.voters.add(request.user)
            voted = True

        # 프론트엔드는 voted 값으로 현재 추천 상태를, vote_count로 추천 수를 갱신할 수 있다.
        return Response({'voted': voted, 'vote_count': question.voters.count()})


class AnswerViewSet(viewsets.ModelViewSet):
    # 답변 목록에서도 작성자/질문/voters를 함께 가져와 불필요한 추가 쿼리를 줄인다.
    queryset = Answer.objects.select_related('author', 'question').prefetch_related('voters').all()
    serializer_class = AnswerSerializer

    # 답변도 조회는 누구나 가능하지만, 작성/수정/삭제는 인증과 작성자 권한을 검사한다.
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        # /api/answers/?question=1 처럼 요청하면 특정 질문의 답변만 필터링한다.
        # 하나의 AnswerViewSet을 전체 답변 조회와 질문별 답변 조회에 함께 사용하기 위한 처리이다.
        queryset = super().get_queryset()
        question_id = self.request.query_params.get('question')
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset

    def create(self, request, *args, **kwargs):
        # 답변은 반드시 어떤 질문에 속해야 하므로 question_id를 먼저 확인한다.
        # URL 경로의 question_id를 우선 사용하고, 없으면 request body의 question 값을 사용한다.
        question_id = kwargs.get('question_id') or request.data.get('question')
        if not question_id:
            return Response({'detail': 'question 값이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # serializer는 입력값 검증을 담당하고, 작성자/부모 질문은 서버에서 직접 지정한다.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, question_id=question_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        # /api/answers/{id}/vote/ 요청을 처리하는 답변 추천/추천취소 API이다.
        answer = self.get_object()

        # 본인 답변 추천을 막는다.
        if answer.author_id == request.user.id:
            return Response({'detail': '본인이 작성한 답변은 추천할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 질문 추천과 동일하게 이미 추천했으면 취소, 아니면 추천으로 토글 처리한다.
        if answer.voters.filter(id=request.user.id).exists():
            answer.voters.remove(request.user)
            voted = False
        else:
            answer.voters.add(request.user)
            voted = True

        return Response({'voted': voted, 'vote_count': answer.voters.count()})