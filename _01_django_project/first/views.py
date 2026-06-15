from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    print(request)
    return HttpResponse('Hello, Django!')

def helloworld(request):
    return HttpResponse('Hello, World!')