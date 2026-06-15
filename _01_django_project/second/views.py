from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse('This is second app!')
    # 응답할 html 문서 경로 작성(templates 폴더 기준 상대경로)
    return render(request, 'second/index.html')