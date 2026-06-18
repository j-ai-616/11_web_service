from django.utils import timezone

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from .models import ChatSession, ChatMessage


load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ('system', '''
너는 IT분야의 직업상담사 챗봇이야.
사용자의 진로 고민에 대해 현실적이고 구체적으로 상담해줘.
'''),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{query}')
])


class DatabaseChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id):
        self.session_id = session_id

        self.session, _ = ChatSession.objects.get_or_create(
            session_id=session_id
        )

    @property
    def messages(self):

        chat_messages = ChatMessage.objects.filter(
            session=self.session
        ).order_by('created_at', 'id')

        messages = []

        for chat_message in chat_messages:
            if chat_message.message_type == 'human':
                messages.append(
                    HumanMessage(content=chat_message.content)
                )
            elif chat_message.message_type == 'ai':
                messages.append(
                    AIMessage(content=chat_message.content)
                )

        return messages

    def add_message(self, message: BaseMessage):

        if isinstance(message, HumanMessage):
            message_type = 'human'
        elif isinstance(message, AIMessage):
            message_type = 'ai'
        else:
            return

        ChatMessage.objects.create(
            session=self.session,
            message_type=message_type,
            content=message.content
        )

        ChatSession.objects.filter(
            id=self.session.id
        ).update(
            updated_at=timezone.now()
        )

    def clear(self):

        ChatMessage.objects.filter(
            session=self.session
        ).delete()

        ChatSession.objects.filter(
            id=self.session.id
        ).update(
            updated_at=timezone.now()
        )


def get_by_session_id(session_id):
    return DatabaseChatMessageHistory(session_id)


llm = init_chat_model('gpt-4.1-mini', temperature=0.7)

chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_by_session_id,
    input_messages_key='query',
    history_messages_key='history'
)


def invoke_chain_with_history(query, session_id):

    return chain_with_history.invoke(
        {'query': query},
        config={
            'configurable': {
                'session_id': session_id
            }
        }
    )