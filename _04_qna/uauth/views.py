from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
from .models import UserForm, UserDetail
from django.db import transaction
from django.http import JsonResponse

# Create your views here.
def logout(request):
    # django auth 앱의 logout 함수를 이용하여 로그아웃 처리
    auth_logout(request)
    # 로그아웃 후에는 index로 리다이렉트
    return redirect('qna:index')

# 트랜잭션 하위에서 예외가 발생하면 모든 DML 작업이 롤백 된다.
# @transaction.atomic
def signup(request):
    if request.method == 'POST':

        # form = UserForm(request.POST)   # POST 데이터로 회원 가입 폼 생성
        # 파일 업로드가 포함 된 form은 request.FILES 도 함께 전달해야 한다.
        form = UserForm(request.POST, request.FILES)    

        if form.is_valid():                 # 폼 유효성 검사

            # 트랜잭션 블럭을 통해 최소화 된 범위에서 트랜잭션 적용
            with transaction.atomic():
                user = form.save(commit=True)   # 모델로 변환하고 DB에 저장 (commit=False는 모델 변환만 수행)
                userdetail = UserDetail(
                    user=user,
                    birthday=form.cleaned_data.get('birthday'),
                    profile=form.cleaned_data.get('profile'),
                )
                userdetail.save()

            # 회원가입 후 로그인 처리
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # 사용자 인증
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                # 로그인 처리
                auth_login(request, authenticated_user)
            return redirect('qna:index')
    else:
        form = UserForm()       # 회원 가입 폼 생성
    
    return render(request, 'uauth/signup.html', {'form':form})  # 회원 가입 페이지 렌더링

def check_username(request):
    username = request.GET.get('username')
    is_exists = User.objects.filter(username=username).exists()

    if is_exists:
        return JsonResponse({'available': False, 'message': '이미 사용 중인 아이디입니다.'})
    
    return JsonResponse({'available': True, 'message': '사용 가능한 아이디입니다.'})