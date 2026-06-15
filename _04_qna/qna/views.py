from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, QuestionForm
from django.core.paginator import Paginator

def index(request):
    # DB에서 질문 목록 조회
    # questions = Question.objects.all()

    # DB에서 페이징 처리 된 목록 조회
    # https://docs.djangoproject.com/ko/6.0/ref/paginator/

    # 최신순 조회
    # questions = Question.objects.order_by('-created_at')
    # N + 1 이슈 해결: question 조회 시점에 answer도 함께 조회할 수 있도록 수정
    questions = Question.objects.prefetch_related('answer').order_by('-created_at')

    print(f'{ questions = }')

    page = request.GET.get('page', 1)       # 요청 페이지 (기본 값: 1)
    paginator = Paginator(questions, 10)    # 한 페이지 당 게시물 개수
    page_obj = paginator.get_page(page)     # 현재 페이지 객체(내용, 메타정보 포함)

    # return render(request, 'qna/index.html', {'questions': questions})
    return render(request, 'qna/index.html', {'page_obj': page_obj})

def question_detail(request, question_id):
    print(f'{ question_id = }')

    # DB에서 question_id에 맞는 질문 조회
    question = get_object_or_404(Question, id=question_id)
    print(f'{ question = }')
    # 질문 객체를 통해 답변 리스트 조회
    answers = question.answer.all()
    print(f'{ answers = }')

    return render(request, 'qna/question_detail.html', {
        'question' : question,
        'answers' : answers
    })

def answer_create(request, question_id):
    # 답변 등록은 POST 요청일 때만 처리한다.
    if request.method != 'POST':
        return redirect('qna:question_detail', question_id=question_id)
    
    print(f'{question_id = }')
    content = request.POST.get('content')
    print(f'{content = }')

    question = get_object_or_404(Question, id=question_id)

    answer = Answer.objects.create(
        content=content,
        question=question
    )

    print(f'{question_id}번 질문에 대한 {answer.id}번 답변이 생성 되었습니다.')

    # POST 요청 후에는 redirect 처리하여 새로고침 시 중복 등록을 방지한다.
    return redirect('qna:question_detail', question_id=question_id)

def answer_delete(request, answer_id):
    if request.method != 'POST':
        return redirect('qna:index')

    print(f'{answer_id = }')

    answer = get_object_or_404(Answer, id=answer_id)
    question_id = answer.question.id

    print(f'{question_id = }')

    answer.delete()

    print(f'{answer_id}번 답변이 삭제되었습니다.')

    return redirect('qna:question_detail', question_id=question_id)


def question_create(request):
    if request.method == 'POST':
        # POST 방식의 요청
        
        # 요청에 담긴 subject와 content가 model Question으로 옮겨지며 변환 됨
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 사용자 입력 값이 유효한 경우
            # 모델 변환 및 DB 저장
            question = form.save()

            print(f'질문 {question.id}번이 등록 되었습니다.')

            return redirect('qna:question_detail', question_id=question.id)
        else:
            # 사용자 입력 값이 유효하지 않은 경우
            print(f'{form.errors=}')

    else:
        # GET 방식의 요청
        form = QuestionForm()

    return render(request, 'qna/question_form.html', {'form':form})