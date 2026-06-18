from django.urls import path
from app import views 

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('set_session/', views.set_session, name='set_session'),
    path('modify_session/', views.modify_session, name='modify_session'),
    path('delete_session/', views.delete_session, name='delete_session'),
    path('set_cookie/', views.set_cookie, name='set_cookie'),
    path('delete_cookie/', views.delete_cookie, name='delete_cookie'),
]