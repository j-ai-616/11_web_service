from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, QuestionForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.http import JsonResponse

def index(request):
    # DB에서 질문 목록 조회
    # questions = Question.objects.all()

    # DB에서 페이징 처리 된 목록 조회
    # https://docs.djangoproject.com/ko/6.0/ref/paginator/

    # 최신순 조회
    # questions = Question.objects.order_by('-created_at')
    # N + 1 이슈 해결: question 조회 시점에 answer도 함께 조회할 수 있도록 수정
    # questions = Question.objects.prefetch_related('answer').order_by('-created_at')
    # question 조회 시점에 answer, author를 함께 조회할 수 있도록 수정
    questions = Question.objects.prefetch_related('answer').select_related('author').order_by('-created_at')

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

@login_required(login_url='uauth:login')
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
        question=question,
        author=request.user
    )

    print(f'{question_id}번 질문에 대한 {answer.id}번 답변이 생성 되었습니다.')

    # POST 요청 후에는 redirect 처리하여 새로고침 시 중복 등록을 방지한다.
    return redirect('qna:question_detail', question_id=question_id)

@login_required(login_url='uauth:login')
def answer_delete(request, answer_id):
    if request.method != 'POST':
        return redirect('qna:index')

    print(f'{answer_id = }')
    answer = get_object_or_404(Answer, id=answer_id)

    # 삭제 권한 검사
    if request.user != answer.author and not request.user.is_staff:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question_id)

    question_id = answer.question.id
    print(f'{question_id = }')

    answer.delete()
    print(f'{answer_id}번 답변이 삭제되었습니다.')

    # 사용자 메세지 처리
    messages.success(request, '답변을 정상적으로 삭제했습니다.')
    return redirect('qna:question_detail', question_id=question_id)

@login_required(login_url='uauth:login')
def question_create(request):

    if request.method == 'POST':    # POST 방식의 요청
        
        # 요청에 담긴 subject와 content가 model Question으로 옮겨지며 변환 됨
        form = QuestionForm(request.POST)

        # 사용자 입력 값이 유효한 경우
        if form.is_valid():
            
            # 모델 변환 및 DB 저장
            # question = form.save()

            # 질문 작성자 포함하여 DB 저장
            question = form.save(commit=False)  # 모델 변환만 수행
            question.author = request.user      # 현재 인증 된 사용자 
            question.save()                     # DB 저장

            print(f'질문 {question.id}번이 등록 되었습니다.')

            return redirect('qna:question_detail', question_id=question.id)
        else:
            # 사용자 입력 값이 유효하지 않은 경우
            print(f'{form.errors=}')

    else:
        # GET 방식의 요청
        form = QuestionForm()

    return render(request, 'qna/question_form.html', {'form':form})

@login_required(login_url='uauth:login')
def question_modify(request, question_id):

    # 원본 조회
    question = Question.objects.get(id=question_id)

    # 수정 권한 검사: 작성자 본인 또는 관리자에 한해 수정 가능
    if request.user != question.author and not request.user.is_staff:
        return HttpResponseForbidden('수정 권한이 없습니다.')
    
    if request.method == 'POST':
        # 원본 객체에 요청을 통해 전달 된 subject, content 업데이트
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('qna:question_detail', question_id=question.id)
    else:
        # 수정 화면 응답 시에는 원본 데이터를 넣고 폼 객체 생성
        form = QuestionForm(instance=question)

    return render(request, 'qna/question_form.html', {'form':form})

# messages 프레임워크 레벨
# messages.success()
# messages.error()
# messages.warning()
# messages.info()
@login_required(login_url='uauth:login')
def question_delete(request, question_id):

    # 원본
    question = Question.objects.get(id=question_id)

    # 삭제 권한 검사
    if request.user != question.author and not request.user.is_staff:
        # return HttpResponseForbidden('삭제 권한이 없습니다.')
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question.id)
    
    question.delete()

    return redirect('qna:index')

# 답변 수정에 필요한 인증, 인가
# 요청 값 꺼내 DB 저장, 응답 처리
@login_required(login_url='uauth:login')
def answer_modify(request, answer_id):
    if request.method != 'POST':
        return redirect('qna:index')
    
    # 원본 조회
    answer = get_object_or_404(Answer, id=answer_id)
    question_id = answer.question.id

    # 수정 권한 검사
    if request.user != answer.author and not request.user.is_staff:
        messages.error(request, '해당 답변 수정 권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question_id)
    
    # 내용 수정
    answer.content = request.POST.get('content')
    answer.save()

    # 사용자 메세지 처리
    messages.success(request, '답변 수정이 완료되었습니다.')
    # return redirect('qna:question_detail', question_id=question_id)

    # 수정한 답변을 참조하는 위치로 응답하기
    url = reverse('qna:question_detail', kwargs={'question_id' : question_id})
    return redirect(f'{url}#answer_{answer.id}')

@login_required(login_url='uauth:login')
@require_POST
def question_vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # 인가/정책 검사: 본인이 작성한 질문은 추천하지 못하게 처리
    if request.user == question.author:
        return JsonResponse({
            'success' : False,
            'message' : '본인이 작성한 질문은 추천할 수 없습니다.',
            'vote_count' : question.voters.count()
        }, status=403)
    
    # 이미 추천한 사용자가 다시 누르면 추천 취소
    if question.voters.filter(id=request.user.id).exists():
        question.voters.remove(request.user)
        voted = False
        message = '질문 추천을 취소했습니다.'
    else:
        question.voters.add(request.user)
        voted = True
        message = '질문을 추천했습니다.'

    return JsonResponse({
        'success' : True,
        'message' : message,
        'voted' : voted,
        'vote_count' : question.voters.count()
    })

@login_required(login_url='uauth:login')
@require_POST
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    # 인가/정책 검사: 본인이 작성한 답변은 추천하지 못하게 처리
    if request.user == answer.author:
        return JsonResponse({
            'success' : False,
            'message' : '본인이 작성한 답변은 추천할 수 없습니다.',
            'vote_count' : answer.voters.count()
        }, status=403)
    
    # 이미 추천한 사용자가 다시 누르면 추천 취소
    if answer.voters.filter(id=request.user.id).exists():
        answer.voters.remove(request.user)
        voted = False
        message = '답변 추천을 취소했습니다.'
    else:
        answer.voters.add(request.user)
        voted = True
        message = '답변을 추천했습니다.'

    return JsonResponse({
        'success' : True,
        'message' : message,
        'voted' : voted,
        'vote_count' : answer.voters.count()
    })