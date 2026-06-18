from django.shortcuts import render, redirect
from datetime import datetime

def index(request):
    return render(request, 'app/index.html')

def set_session(request):
    # POST 요청으로 받은 데이터를 세션에 저장
    username = request.POST.get('username')
    request.session['username'] = username

    # 파이썬의 모든 타입 저장 가능
    request.session['point'] = 1234567890
    request.session['prob'] = 12345.6789
    request.session['expired'] = True
    request.session['nums'] = [1, 2, 3, 4, 5]
    request.session['data'] = {
        'today' : datetime.now().strftime('%Y-%m-%d'),
        'message' : '안녕 세션'
    }

    # 세션 유효기간 설정 (전역 설정 override)
    # request.session.set_expiry(10)      # 10초 후 만료

    return redirect('app:index')

def modify_session(request):
    # 새 속성 추가/변경
    # - 세션 객체의 최상위 키 변경은 자동으로 감지
    # request.session['favorite_color'] = 'springgreen'

    # - 중첩 된 속성 변경 시는 명시적으로 변경 됨을 알려야 함
    request.session['nums'].append(999)
    request.session['data']['new_item'] = '새로운 데이터'
    request.session.modified = True

    # 속성 제거
    del request.session['point']

    return redirect('app:index')

def delete_session(request):
    # 세션 객체/쿠키 삭제
    request.session.flush()
    return redirect('app:index')

def set_cookie(request):
    name = request.POST.get('cookie_name')
    value = request.POST.get('cookie_value')

    # 쿠키는 response 객체에 담아서 보낸다.
    response = redirect('app:index')

    response.set_cookie(
        name, value,
        max_age=60,             # 60초간 영속하는 쿠키, 지정하지 않으면 세션 쿠키
        path='/app/',           # 해당 경로 아래의 요청일 때만 전송
        httponly=True,          # JS로 접근 불가
        samesite='Lax',         # 타 사이트에서 쿠키 요청 시 전송 하지 않음
        secure=False            # secure=True일 때 HTTPS 에서만 전송 가능
    )

    return response

def delete_cookie(request):
    response = redirect('app:index')
    name = request.POST.get('cookie_name')
    response.delete_cookie(name, path='/app/')  # max_age=0 으로 set_cookie 전달
    return response