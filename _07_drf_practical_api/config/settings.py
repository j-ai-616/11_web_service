from pathlib import Path
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-for-class')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DRF는 Django 모델/View를 REST API로 만들기 위한 앱이다.
    'rest_framework',
    # JWT 로그인/토큰 재발급 기능을 제공한다.
    'rest_framework_simplejwt',
    # OpenAPI 스키마와 Swagger 문서를 자동 생성한다.
    'drf_spectacular',
    # 프론트 서버와 API 서버의 origin이 다를 때 CORS 정책을 제어한다.
    'corsheaders',

    'accounts',
    'qna',
    'chatbot',
]

MIDDLEWARE = [
    # CORS 헤더는 가능한 앞쪽 middleware에서 처리해야 한다.
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # 기본 인증 방식을 JWT로 지정하면 Authorization 헤더의 Bearer 토큰으로 사용자를 식별한다.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 기본 권한은 열어두고, 각 ViewSet에서 기능별 권한을 명시한다.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # 페이지네이션은 목록 API 응답을 일정 크기로 나누어 반환한다.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # Swagger 문서 생성기를 DRF의 schema backend로 등록한다.
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Throttling은 API 요청 횟수를 제한해 남용과 LLM 비용 증가를 줄인다.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/min',
        'user': '120/min',
        'chatbot': os.getenv('CHATBOT_THROTTLE_RATE', '5/min'),
    },
}

SIMPLE_JWT = {
    # access token은 짧게, refresh token은 상대적으로 길게 두는 것이 일반적이다.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': '_07 DRF Practical API',
    'DESCRIPTION': 'QnA, JWT 인증, Swagger, 권한, Throttling, Chatbot API 실습 프로젝트',
    'VERSION': '1.0.0',
}

# 개발 중에는 로컬 프론트 서버만 명시적으로 허용한다.
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

# JWT 기반 API는 보통 CSRF 토큰이 아니라 Authorization 헤더로 인증한다.
# 단, Django Admin이나 세션 기반 화면은 기존 CSRF 보호가 그대로 필요하다.
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]
