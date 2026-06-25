# Django 개요 및 기본 명령어

## 1. Django란?

Django는 Python 기반의 웹 프레임워크이다.
웹 서비스를 만들 때 자주 필요한 기능을 미리 제공하여, 개발자가 비즈니스 로직에 더 집중할 수 있도록 도와준다.

Django는 다음과 같은 기능을 기본적으로 제공한다.

- URL 요청을 처리하는 URL 라우팅
- 요청을 받아 응답을 만드는 View
- HTML 화면을 구성하는 Template
- 데이터베이스와 Python 코드를 연결하는 ORM
- 관리자 페이지(Admin)
- 사용자 인증, 세션, 보안 기능

즉, Django는 단순히 HTML을 보여주는 도구가 아니라 **웹 애플리케이션의 전체 구조를 빠르게 구성할 수 있게 해 주는 프레임워크**이다.


## 2. Django를 배우는 이유

웹 백엔드 개발에서는 다음과 같은 작업이 반복적으로 필요하다.

- 사용자의 요청 URL을 구분한다.
- 요청에 맞는 Python 함수를 실행한다.
- 필요한 데이터를 조회하거나 저장한다.
- HTML 또는 JSON 형태로 응답을 반환한다.
- 로그인, 관리자 페이지, 데이터베이스 연동을 처리한다.

Django는 이런 반복 작업을 구조화된 방식으로 제공한다.
따라서 백엔드 개발의 기본 흐름을 이해하기 좋고, 이후 REST API, 인증, 배포까지 자연스럽게 확장할 수 있다.


## 3. Django의 기본 구조

Django 프로젝트는 크게 **프로젝트(project)** 와 **앱(app)** 으로 나누어 생각한다.

### 프로젝트(Project)

프로젝트는 하나의 웹 서비스 전체 설정을 담당한다.
예를 들어 사이트 전체 설정, 데이터베이스 설정, URL 최상위 연결, 배포 설정 등이 프로젝트에 포함된다.

예시:

```text
django_project/
├─ manage.py
├─ django_project/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
└─ post/
```

### 앱(App)

앱은 프로젝트 안에서 특정 기능 단위를 담당한다.
예를 들어 게시글 기능, 회원 기능, 댓글 기능, 상품 기능 등을 각각 앱으로 나눌 수 있다.

예시:

```text
post/
├─ admin.py
├─ apps.py
├─ models.py
├─ tests.py
├─ views.py
└─ urls.py
```

정리하면 다음과 같다.

| 구분 | 역할 |
|---|---|
| Project | 웹 서비스 전체 설정 |
| App | 기능 단위 구현 |
| manage.py | Django 명령어 실행 파일 |
| settings.py | 프로젝트 설정 파일 |
| urls.py | URL 연결 설정 |
| views.py | 요청 처리 로직 |
| models.py | 데이터베이스 테이블과 연결되는 모델 |
| templates | HTML 파일 저장 위치 |
| static | CSS, JS, 이미지 파일 저장 위치 |


## 4. 프로젝트 생성

```bash
django-admin startproject django_project
```

위 명령어는 `django_project`라는 Django 프로젝트를 생성한다.

생성 후 폴더 구조는 대략 다음과 같다.

```text
django_project/
├─ manage.py
└─ django_project/
   ├─ __init__.py
   ├─ settings.py
   ├─ urls.py
   ├─ asgi.py
   └─ wsgi.py
```

### 프로젝트 폴더로 이동

```bash
cd django_project
```

Django의 대부분 명령어는 `manage.py`가 있는 위치에서 실행한다.


## 5. 개발 서버 실행

```bash
python manage.py runserver
```

서버가 실행되면 브라우저에서 아래 주소로 접속한다.

```text
http://127.0.0.1:8000/
```

개발 서버를 종료할 때는 터미널에서 `Ctrl + C`를 누른다.

### 포트 번호를 바꿔 실행하기

```bash
python manage.py runserver 8001
```

기본 포트인 `8000`번을 이미 사용 중이라면 다른 포트 번호로 실행할 수 있다.

## 6. 앱 생성

```bash
python manage.py startapp post
```

위 명령어는 `post`라는 앱을 생성한다.

생성 후 폴더 구조는 다음과 같다.

```text
post/
├─ __init__.py
├─ admin.py
├─ apps.py
├─ migrations/
│  └─ __init__.py
├─ models.py
├─ tests.py
└─ views.py
```

앱을 생성한 뒤에는 보통 `settings.py`의 `INSTALLED_APPS`에 앱을 등록한다.

```python
INSTALLED_APPS = [
    # 생략
    'post',
]
```


## 7. 기본 요청 처리 흐름

Django에서 사용자가 페이지에 접속하면 대략 다음 흐름으로 처리된다.

```text
브라우저 요청
    ↓
프로젝트 urls.py
    ↓
앱 urls.py
    ↓
views.py
    ↓
HTML 또는 문자열 응답
    ↓
브라우저 화면 출력
```

예를 들어 `/post/` 주소로 요청이 들어오면 다음과 같은 흐름이 된다.

```text
http://127.0.0.1:8000/post/
    ↓
프로젝트 urls.py에서 post 앱으로 연결
    ↓
post/urls.py에서 특정 view 함수로 연결
    ↓
post/views.py의 함수 실행
    ↓
HttpResponse 또는 render 결과 반환
```


## 8. URL 연결 기본 예시

### 프로젝트 urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
]
```

`include()`는 특정 URL 경로 이후의 처리를 앱의 `urls.py`로 넘길 때 사용한다.

### 앱 urls.py

앱 폴더 안에 `urls.py` 파일을 직접 생성한다.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
]
```

### 앱 views.py

```python
from django.http import HttpResponse


def index(request):
    return HttpResponse('첫 번째 Django 페이지입니다.')
```

브라우저에서 아래 주소로 접속하면 문자열 응답이 출력된다.

```text
http://127.0.0.1:8000/post/
```


## 9. Template 사용 기본 흐름

문자열을 직접 반환하는 대신 HTML 파일을 반환하려면 template을 사용한다.

### templates 폴더 예시

```text
django_project/
├─ templates/
│  └─ post/
│     └─ index.html
├─ post/
└─ manage.py
```

### settings.py 설정 예시

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### views.py 예시

```python
from django.shortcuts import render


def index(request):
    return render(request, 'post/index.html')
```


## 10. 데이터베이스와 마이그레이션

Django는 모델 클래스를 작성한 뒤, 이를 데이터베이스 테이블로 반영하는 과정을 제공한다.
이때 사용하는 개념이 **마이그레이션(Migration)** 이다.

### 모델 변경 파일 생성

```bash
python manage.py makemigrations
```

`models.py`의 변경 내용을 바탕으로 migration 파일을 생성한다.

### 데이터베이스에 반영

```bash
python manage.py migrate
```

생성된 migration 파일을 실제 데이터베이스에 적용한다.

일반적인 순서는 다음과 같다.

```text
models.py 수정
    ↓
python manage.py makemigrations
    ↓
python manage.py migrate
    ↓
DB 테이블 생성 또는 변경
```


## 자주 사용하는 명령어 정리

| 목적 | 명령어 |
|---|---|
| Django 설치 | `pip install django` |
| Django 버전 확인 | `python -m django --version` |
| 프로젝트 생성 | `django-admin startproject 프로젝트명` |
| 프로젝트 폴더 이동 | `cd 프로젝트명` |
| 앱 생성 | `python manage.py startapp 앱명` |
| 개발 서버 실행 | `python manage.py runserver` |
| 포트 변경 실행 | `python manage.py runserver 8001` |
| migration 파일 생성 | `python manage.py makemigrations` |
| DB 반영 | `python manage.py migrate` |
| 관리자 계정 생성 | `python manage.py createsuperuser` |
| Django shell 실행 | `python manage.py shell` |
| 테스트 실행 | `python manage.py test` |


## 핵심

Django를 처음 배울 때는 모든 기능을 한 번에 이해하려고 하기보다 다음 흐름을 먼저 잡는 것이 중요하다.

```text
프로젝트 생성
    ↓
앱 생성
    ↓
URL 연결
    ↓
View 작성
    ↓
Template 연결
    ↓
Model 작성
    ↓
Migration 실행
    ↓
Admin 또는 ORM으로 데이터 확인
```

특히 초반에는 다음 세 가지 파일의 역할을 구분하는 것이 중요하다.

| 파일 | 핵심 역할 |
|---|---|
| urls.py | 어떤 주소로 들어온 요청인지 판단한다. |
| views.py | 요청을 처리하고 응답을 만든다. |
| models.py | 데이터베이스 테이블 구조를 Python 클래스로 정의한다. |

Django의 기본 학습 흐름은 결국 **URL → View → Template → Model** 구조를 반복해서 익히는 과정이다.
