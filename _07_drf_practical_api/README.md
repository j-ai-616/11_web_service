# _07_drf_practical_api

기존 Django QnA/챗봇 흐름을 DRF 기반 REST API 서버로 확장한 프로젝트이다.

## 포함 기능

1. Question API
2. Answer API
3. JWT 로그인
4. 작성자 권한
5. Swagger
6. CORS/CSRF/Throttling
7. Chatbot API
8. 사용자별 채팅 세션
9. API 테스트

## 실행 순서

```bash
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 주요 URL

```text
POST /api/auth/register/
POST /api/auth/token/
POST /api/auth/token/refresh/
GET  /api/auth/me/

GET    /api/questions/
POST   /api/questions/
GET    /api/questions/{id}/
PATCH  /api/questions/{id}/
DELETE /api/questions/{id}/
POST   /api/questions/{id}/vote/

POST   /api/questions/{question_id}/answers/
GET    /api/answers/?question={question_id}
PATCH  /api/answers/{id}/
DELETE /api/answers/{id}/
POST   /api/answers/{id}/vote/

GET    /api/chat/sessions/
POST   /api/chat/sessions/
GET    /api/chat/sessions/{id}/messages/
POST   /api/chat/sessions/{id}/send/
DELETE /api/chat/sessions/{id}/

GET /api/docs/
```

## 테스트

```bash
python manage.py test
```

---
# _07_drf_practical_api 개념 정리

## 1. DRF와 REST API

DRF(Django REST Framework)는 Django로 REST API를 만들기 위한 대표적인 도구이다. 
기존 Django View가 HTML을 렌더링했다면, DRF View는 JSON 데이터를 응답한다.

기존 템플릿 기반 응답은 보통 다음 흐름이다.

```text
사용자 요청 → View → Template 렌더링 → HTML 응답
```

DRF 기반 API 응답은 다음 흐름이다.

```text
클라이언트 요청 → ViewSet/APIView → Serializer → JSON 응답
```

REST API는 프론트엔드, 모바일 앱, 외부 서비스, AI 서비스 등 다양한 클라이언트가 서버 기능을 사용할 수 있도록 HTTP 기반 인터페이스를 제공한다.


## 2. Serializer

Serializer는 Django 모델 객체와 JSON 데이터 사이를 변환하는 역할을 한다. 또한 사용자가 보낸 입력값이 유효한지도 검사한다.

주요 역할은 다음과 같다.

```text
모델 객체 → JSON 응답 데이터
JSON 요청 데이터 → 검증된 Python 데이터
검증된 데이터 → 모델 객체 생성/수정
```

`ModelSerializer`는 Django 모델을 기반으로 serializer 필드를 자동 구성해준다. 이번 프로젝트에서는 `Question`, `Answer`, `ChatSession`, `ChatMessage` 모델을 API 응답으로 변환할 때 사용한다.


## 3. ViewSet과 Router

`ViewSet`은 목록 조회, 상세 조회, 생성, 수정, 삭제 기능을 하나의 클래스로 묶는 방식이다.

일반적인 CRUD API는 다음 HTTP method와 연결된다.

| HTTP method | 의미 |
|---|---|
| GET | 목록/상세 조회 |
| POST | 생성 |
| PUT/PATCH | 수정 |
| DELETE | 삭제 |

`Router`는 ViewSet을 등록하면 REST API URL을 자동 생성해준다.

예를 들어 `QuestionViewSet`을 `questions`로 등록하면 다음과 같은 URL이 생성된다.

```text
GET    /api/questions/
POST   /api/questions/
GET    /api/questions/{id}/
PATCH  /api/questions/{id}/
DELETE /api/questions/{id}/
```

---

## 4. JWT 인증

JWT(JSON Web Token)는 API 서버에서 자주 사용하는 토큰 기반 인증 방식이다. 기존 Django 템플릿 웹앱에서는 로그인 후 `sessionid` 쿠키를 사용했지만, REST API에서는 보통 `Authorization` 헤더에 토큰을 담아 요청한다.

요청 예시는 다음과 같다.

```http
Authorization: Bearer <access_token>
```

이번 프로젝트에서는 `djangorestframework-simplejwt`를 사용한다.

주요 endpoint는 다음과 같다.

```text
POST /api/auth/token/          로그인, access/refresh token 발급
POST /api/auth/token/refresh/  refresh token으로 access token 재발급
GET  /api/auth/me/             현재 로그인 사용자 정보 조회
```

`access token`은 실제 API 요청 인증에 사용하고, `refresh token`은 access token이 만료되었을 때 새 access token을 발급받는 데 사용한다.

---

## 5. Permission과 작성자 권한

Permission은 API 요청을 허용할지 거부할지 판단하는 규칙이다.

이번 프로젝트에서는 다음 권한 규칙을 적용한다.

```text
질문 목록/상세 조회: 누구나 가능
질문 작성: 로그인 사용자만 가능
질문 수정/삭제: 작성자만 가능
답변 작성: 로그인 사용자만 가능
답변 수정/삭제: 작성자만 가능
채팅 세션 조회/삭제: 본인만 가능
챗봇 메시지 전송: 본인 세션에서만 가능
```

DRF에서는 `permission_classes`를 통해 View 단위 권한을 설정하고, `has_object_permission()`을 통해 특정 객체에 대한 수정/삭제 권한을 검사할 수 있다.

---

## 6. Swagger와 OpenAPI

Swagger는 API 문서를 브라우저에서 확인하고 직접 요청까지 테스트할 수 있게 해주는 도구이다. 이번 프로젝트에서는 `drf-spectacular`를 사용한다.

주요 URL은 다음과 같다.

```text
/api/schema/  OpenAPI 스키마 JSON/YAML
/api/docs/    Swagger UI 화면
```

Swagger를 사용하면 API 목록, 요청 body, 응답 schema, 인증 필요 여부를 한눈에 확인할 수 있다. 실무에서는 백엔드 개발자와 프론트엔드 개발자 사이의 API 명세 공유에 자주 사용된다.

---

## 7. CORS와 CSRF

CORS는 서로 다른 origin 사이에서 브라우저가 API 요청을 허용할지 판단하는 보안 정책이다.

예를 들어 프론트엔드가 `http://localhost:5173`에서 실행되고, 백엔드 API가 `http://127.0.0.1:8000`에서 실행되면 브라우저 입장에서는 서로 다른 origin이다. 이 경우 백엔드에서 해당 origin을 허용해야 API 요청이 정상 처리된다.

CSRF는 사용자가 의도하지 않은 요청을 보내게 만드는 공격을 방어하기 위한 개념이다. Django의 세션/쿠키 기반 인증에서는 CSRF 보호가 중요하다. 반면 JWT 기반 API에서는 일반적으로 쿠키의 세션 인증 대신 `Authorization` 헤더를 사용하므로 CSRF 처리 방식이 달라진다.

중요한 점은 다음이다.

```text
세션 기반 화면: CSRF 보호 필요
JWT 기반 API: Authorization 헤더 기반 인증 사용
Django Admin: 기존 CSRF 보호 유지
```

---

## 8. Throttling

Throttling은 일정 시간 동안 허용할 API 요청 횟수를 제한하는 기능이다. 게시판 API에서도 남용 방지에 도움이 되지만, 특히 챗봇 API처럼 외부 LLM 비용이 발생할 수 있는 기능에서는 더 중요하다.

이번 프로젝트에서는 전체 API 기본 제한과 별도로 챗봇 메시지 전송 API에 `chatbot` scope를 적용한다.

예시는 다음과 같다.

```text
일반 로그인 사용자: 120/min
챗봇 메시지 전송: 5/min
```

---

## 9. 사용자별 채팅 세션

기존 챗봇 예제는 세션 ID를 기준으로 대화 기록을 구분했다. 이번 프로젝트에서는 실무 API 구조에 맞게 `ChatSession`이 사용자와 직접 연결된다.

구조는 다음과 같다.

```text
User 1 : N ChatSession
ChatSession 1 : N ChatMessage
```

따라서 사용자는 본인의 채팅 세션만 조회할 수 있고, 다른 사용자의 세션 메시지는 조회할 수 없다.

---

## 10. API 테스트

이번 프로젝트에서는 DRF의 `APITestCase`를 사용해 API 동작을 검증한다.

테스트 대상은 다음과 같다.

```text
회원가입 API
JWT 로그인 API
비로그인 질문 작성 실패
로그인 질문 작성 성공
작성자 수정 성공
다른 사용자 수정 실패
답변 작성 성공
본인 채팅 세션만 조회
챗봇 메시지 전송 시 human/ai 메시지 저장
```

API 테스트는 단순히 코드가 실행되는지 확인하는 것이 아니라, 인증/권한/응답 상태코드/DB 변경 결과가 의도대로 동작하는지 검증하는 과정이다.


