from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound

import uuid
import json

from .models import ChatSession, ChatMessage
from .chatbot_service import invoke_chain_with_history


def index(request):
    return render(request, 'app/index.html')


@csrf_exempt
@require_POST
def init_conversation(request):

    session_id = str(uuid.uuid4())

    ChatSession.objects.create(
        session_id=session_id
    )

    return JsonResponse({
        'session_id': session_id
    }, status=201)


@csrf_exempt
@require_POST
def chatbot(request):

    session_id = request.POST.get('session_id')
    query = request.POST.get('query')

    if not session_id or not query:
        return HttpResponseBadRequest('session_id and query are required!')

    if not ChatSession.objects.filter(session_id=session_id).exists():
        return HttpResponseNotFound('Invalid session_id')

    response = invoke_chain_with_history(query, session_id)

    return JsonResponse({
        'content': response.content
    })


@csrf_exempt
@require_http_methods(['DELETE'])
def remove_conversation(request):

    try:
        body = json.loads(request.body)
        session_id = body.get('session_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON body')

    if not session_id:
        return HttpResponseBadRequest('session_id is required!')

    try:
        session = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return HttpResponseNotFound('Session id not found')

    session.delete()

    return JsonResponse({
        'result': 'success',
        'message': f'Conversation with session_id {session_id} removed!'
    })


@require_GET
def get_session_list(request):

    sessions = ChatSession.objects.all().order_by('-updated_at')

    session_list = [
        session.session_id
        for session in sessions
    ]

    return JsonResponse({
        'session_list': session_list
    })


@require_GET
def get_conversation_messages(request):

    session_id = request.GET.get('session_id')

    if not session_id:
        return HttpResponseBadRequest('session_id is required!')

    try:
        session = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return HttpResponseNotFound('Invalid session_id')

    chat_messages = ChatMessage.objects.filter(
        session=session
    ).order_by('created_at', 'id')

    messages = []

    for message in chat_messages:
        messages.append({
            'type': message.message_type,
            'content': message.content,
            'created_at': message.created_at.isoformat()
        })

    return JsonResponse({
        'session_id': session_id,
        'messages': messages
    })