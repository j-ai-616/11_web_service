import os
from django.utils import timezone

from .models import ChatMessage, ChatSession


SYSTEM_PROMPT = '너는 Django와 백엔드 개발 학습을 돕는 실무형 튜터이다.'


def _fallback_response(user_message):
    # 테스트/수업 환경에서는 외부 LLM 키 없이도 API 흐름을 검증할 수 있도록 fallback 응답을 둔다.
    return f'[테스트 응답] 질문을 받았습니다: {user_message}'


def _invoke_openai_if_enabled(history, user_message):
    # 외부 API 호출은 서비스 함수로 분리해 View가 비즈니스 로직에 직접 의존하지 않게 한다.
    use_llm = os.getenv('CHATBOT_USE_LLM', 'False') == 'True'
    if not use_llm:
        return _fallback_response(user_message)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        for item in history:
            role = 'user' if item.message_type == 'human' else 'assistant'
            messages.append({'role': role, 'content': item.content})
        messages.append({'role': 'user', 'content': user_message})

        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as exc:
        return f'[LLM 호출 실패] {exc}'


def send_message(session: ChatSession, user_message: str):
    # 사용자 메시지 저장 -> AI 응답 생성 -> AI 메시지 저장 순서로 하나의 API 작업을 구성한다.
    history = list(session.messages.all())

    human_message = ChatMessage.objects.create(
        session=session,
        message_type='human',
        content=user_message,
    )

    ai_content = _invoke_openai_if_enabled(history, user_message)
    ai_message = ChatMessage.objects.create(
        session=session,
        message_type='ai',
        content=ai_content,
    )

    session.updated_at = timezone.now()
    if session.title == '새 채팅':
        session.title = user_message[:30]
    session.save(update_fields=['updated_at', 'title'])

    return human_message, ai_message
