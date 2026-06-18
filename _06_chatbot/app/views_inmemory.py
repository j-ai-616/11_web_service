from django.shortcuts import render
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import uuid
import json

load_dotenv()

# LLM에 전달할 프롬프트 구조 정의
prompt = ChatPromptTemplate.from_messages([
    ('system', '너는 IT분야의 직업상담사 챗봇이야.'),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{query}')
])

# 세션별 대화 기록을 저장할 딕셔너리(key:session_id, value:대화 기록 객체)
store = {}

# session_id에 해당하는 대화 기록을 반환
def get_by_session_id(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]

# 사용할 LLM 모델 생성
llm = init_chat_model('gpt-4.1-mini', temperature=0.7)

# 실행 체인 생성
chain = prompt | llm

# chain에 대화 기록 관리 기능 추가
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_by_session_id,
    input_messages_key='query',
    history_messages_key='history'
)

# 대화 기록을 포함해 LLM 체인을 실행하는 함수
def invoke_chain_with_history(query, session_id):

    return chain_with_history.invoke(
        {'query' : query},
        config={
            'configurable': {
                'session_id' : session_id
            }
        }
    )


def index(request):
    return render(request, 'app/index.html')

@csrf_exempt
@require_POST
def init_conversation(request):
    session_id = str(uuid.uuid4())
    get_by_session_id(session_id)
    return JsonResponse({'session_id': session_id})

@csrf_exempt
@require_POST
def chatbot(request):
    session_id = request.POST.get('session_id')
    query = request.POST.get('query')

    # 유효성 검사
    if not session_id or not query:
        return HttpResponseBadRequest('session_id and query are required!')
    if session_id not in store:
        return HttpResponseNotFound('Invalid session_id')
    
    response = invoke_chain_with_history(query, session_id)

    return JsonResponse({
        'content' : response.content
    })

@csrf_exempt
@require_http_methods(['DELETE'])   # 허용할 Htttp Method 설정
def remove_conversation(request):

    try:
        body = json.loads(request.body)     # JSON 문자열 -> Python dict/list로 변환
        session_id = body.get('session_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON body')
    
    if session_id not in store:
        return HttpResponseNotFound('Session id not found')
    
    store.pop(session_id)

    return JsonResponse({
        'result' : 'success',
        'message' : f'Conversation with session_id {session_id} Removed!'
    })

@require_GET
def get_session_list(request):
    return JsonResponse({
        'session_list' : list(store.keys())
    })

@require_GET
def get_conversation_messages(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return HttpResponseBadRequest('session_id is required!')
    
    if session_id not in store:
        return HttpResponseNotFound('Invalid session_id')

    history = store[session_id]

    messages = []
    for message in history.messages:
        messages.append({
            'type' : message.type,
            'content' : message.content
        })

    return JsonResponse({
        'session_id' : session_id,
        'messages' : messages
    })