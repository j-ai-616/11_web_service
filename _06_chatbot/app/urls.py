from django.urls import path
from app import views 

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('init_conversation/', views.init_conversation, name='init_conversation'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('remove_conversation/', views.remove_conversation, name='remove_conversation'),
    path('get_session_list/', views.get_session_list, name='get_session_list'),
    path('get_conversation_messages/', views.get_conversation_messages, name='get_conversation_messages'),
]