from django.urls import path
from . import views

app_name = 'first'

urlpatterns = [
    path('', views.index, name='index'),
    path('helloworld', views.helloworld, name='helloworld')
]