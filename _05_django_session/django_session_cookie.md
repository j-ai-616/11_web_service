# Django Session & Cookie 개념

## 1. 학습 목표

Django에서 HTTP의 무상태성을 보완하기 위해 사용하는 Cookie와 Session을 이해한다.

- HTTP 요청/응답은 기본적으로 상태를 기억하지 않는다.
- Cookie는 브라우저에 저장되는 클라이언트 측 상태 저장 방식이다.
- Session은 서버에 저장되는 서버 측 상태 저장 방식이다.
- Django는 기본적으로 세션 데이터를 DB의 `django_session` 테이블에 저장한다.
- 브라우저는 세션 데이터를 직접 들고 있는 것이 아니라 `sessionid` 쿠키를 들고 있다.
- View에서 `request.session`으로 세션 값을 저장, 조회, 수정, 삭제할 수 있다.
- Response 객체의 `set_cookie()`, `delete_cookie()`로 쿠키를 생성하고 삭제할 수 있다.

## 2. HTTP의 무상태성

HTTP는 기본적으로 무상태(stateless) 프로토콜이다.

무상태란 서버가 이전 요청의 정보를 자동으로 기억하지 않는다는 뜻이다.

```text
1번째 요청: /login/ 접속
2번째 요청: /mypage/ 접속
```

HTTP 자체만 보면 서버는 2번째 요청을 받았을 때 이 사용자가 앞에서 로그인했는지 알 수 없다.

그래서 웹 애플리케이션은 사용자의 상태를 유지하기 위해 Cookie와 Session을 사용한다.

## 3. Cookie와 Session의 차이

| 구분 | Cookie | Session |
|---|---|---|
| 저장 위치 | 브라우저 | 서버 |
| Django에서 접근 | `request.COOKIES` | `request.session` |
| 생성 방식 | `response.set_cookie()` | `request.session['key'] = value` |
| 삭제 방식 | `response.delete_cookie()` | `del`, `flush()` 등 |
| 주요 용도 | 간단한 사용자 설정, 추적 값 | 로그인 상태, 사용자별 임시 데이터 |
| 보안 관점 | 사용자가 볼 수 있음 | 실제 데이터는 서버에 저장됨 |

Cookie는 브라우저가 들고 다니는 값이고, Session은 서버가 보관하는 사용자별 값이다.

Django의 기본 세션 방식에서는 브라우저가 `sessionid` 쿠키만 가지고 있고, 실제 세션 데이터는 서버의 DB에 저장된다.

## 4. Cookie 주요 속성

쿠키는 단순히 이름과 값만 저장하는 것이 아니라, 여러 속성을 함께 가진다.

```python
response.set_cookie(
    'theme',
    'dark',
    max_age=60 * 60 * 24,
    httponly=True,
    samesite='Lax',
)
```

| 속성 | 의미 |
|---|---|
| `key` | 쿠키 이름 |
| `value` | 쿠키 값 |
| `max_age` | 쿠키 유지 시간. 초 단위 |
| `expires` | 쿠키 만료 시각 |
| `path` | 쿠키가 전송될 URL 경로 |
| `domain` | 쿠키가 적용될 도메인 |
| `secure` | HTTPS 요청에서만 쿠키 전송 |
| `httponly` | JavaScript에서 쿠키 접근 차단 |
| `samesite` | 다른 사이트 요청에 쿠키를 보낼지 제한 |

### HttpOnly

`HttpOnly`는 JavaScript에서 쿠키에 접근하지 못하게 하는 설정이다.

```python
httponly=True
```

`True`이면 `document.cookie`로 해당 쿠키를 읽을 수 없다.

XSS 공격으로 쿠키가 탈취되는 위험을 줄이는 데 도움이 된다. 단, XSS 자체를 막는 설정은 아니다.

### SameSite

`SameSite`는 다른 사이트에서 요청이 발생했을 때 쿠키를 함께 보낼지 제한하는 정책이다.

| 값 | 의미 |
|---|---|
| `Lax` | 일반 링크 이동은 허용, 외부 사이트의 POST 요청 등은 제한 |
| `Strict` | 같은 사이트 요청에만 쿠키 전송 |
| `None` | 다른 사이트 요청에도 쿠키 전송 가능. `Secure=True` 필요 |

`SameSite=Lax`는 CSRF를 완전히 막는 설정은 아니지만, CSRF 위험을 줄이는 보조 방어 수단이다.

Django에서는 CSRF 토큰과 함께 사용하는 것이 기본이다.

## 5. Django Session 동작 흐름

Django에서 기본 세션은 다음 순서로 동작한다.

```text
1. 사용자가 서버에 요청을 보낸다.
2. 브라우저는 요청에 sessionid 쿠키를 함께 보낸다.
3. Django의 SessionMiddleware가 sessionid를 확인한다.
4. Django는 django_session 테이블에서 해당 세션 데이터를 찾는다.
5. View에서는 request.session으로 세션 데이터를 사용한다.
6. 세션이 변경되면 응답 과정에서 DB에 저장된다.
```

개발자는 직접 `django_session` 테이블을 조회하지 않아도 된다.
View에서 `request.session`을 사용하면 Django가 내부 처리를 대신 해준다.

## 6. settings.py의 세션 설정

```python
# 세션 데이터 저장 위치
# 기본값: 'django.contrib.sessions.backends.db'
# 옵션: db, cache, cached_db, file, signed_cookies
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 세션 쿠키 유지 시간
# 기본값: 1209600초 = 2주
SESSION_COOKIE_AGE = 1209600

# 브라우저 종료 시 세션 만료 여부
# 기본값: False
# True이면 브라우저 종료 시 세션 만료
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# 매 요청마다 세션 저장 여부
# 기본값: False
# True이면 매 요청마다 세션을 저장할 수 있음
SESSION_SAVE_EVERY_REQUEST = False

# JS에서 세션 쿠키 접근 차단 여부
# 기본값: True
# XSS로 인한 쿠키 탈취 위험을 줄임
SESSION_COOKIE_HTTPONLY = True

# 다른 사이트 요청에 쿠키를 보낼지 제한
# 기본값: 'Lax'
# 옵션: 'Lax', 'Strict', 'None'
# CSRF 위험을 줄이는 보조 방어 수단
SESSION_COOKIE_SAMESITE = 'Lax'
```

### SESSION_ENGINE

세션 데이터를 어디에 저장할지 정한다.

| 값 | 의미 |
|---|---|
| `django.contrib.sessions.backends.db` | DB의 `django_session` 테이블에 저장 |
| `django.contrib.sessions.backends.cache` | 캐시에만 저장 |
| `django.contrib.sessions.backends.cached_db` | 캐시와 DB를 함께 사용 |
| `django.contrib.sessions.backends.file` | 파일에 저장 |
| `django.contrib.sessions.backends.signed_cookies` | 쿠키에 서명된 세션 데이터 저장 |

수업 예제에서는 기본값인 DB 저장 방식을 사용한다.

### SESSION_COOKIE_SAMESITE

`SameSite`는 다른 사이트에서 요청이 발생했을 때 쿠키를 함께 보낼지 제한하는 정책이다.

| 값 | 의미 |
|---|---|
| `Lax` | 일반 링크 이동은 허용, 외부 사이트의 POST 요청 등은 제한 |
| `Strict` | 같은 사이트 요청에만 쿠키 전송 |
| `None` | 다른 사이트 요청에도 쿠키 전송 가능. `Secure=True` 필요 |

`SameSite=Lax`는 CSRF를 완전히 막는 설정은 아니지만, CSRF 위험을 줄이는 보조 방어 수단이다.
