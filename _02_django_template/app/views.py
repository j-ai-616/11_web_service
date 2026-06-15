from django.shortcuts import render
from datetime import datetime

context = {
    'name': 'Django',
    'age': 23,
    'num': 1,
    'hobby': ['coding', 'reading', 'traveling'],
    'today': datetime.now(),
    'is_authenticated': False,
    'fruits': ['apple', 'banana', 'cherry'],
    'users': [
        {'id': 1234, 'name': 'Alice', 'age': 24, 'married': True},
        {'id': 2345, 'name': 'Bob', 'age': 34, 'married': False},
        {'id': 3456, 'name': 'Charlie', 'age': 25, 'married': True},
    ],
    # 'users': [],
}

# Create your views here.
def index(request):
    return render(request, 'app/index.html')

def _01_variables_filters(request):
    return render(request, 'app/01_variables_filters.html', context)

def _02_tags(request):
    return render(request, 'app/02_tags.html', context)

def _03_layout(request):
    return render(request, 'app/03_layout.html', context)

def _04_staticfiles(request):
    return render(request, 'app/04_staticfiles.html', context)

def _05_urls(request):
    return render(request, 'app/05_urls.html', context)

def _06_bootstrap(request):
    return render(request, 'app/06_bootstrap.html')

def articles_detail(request, id):
    print(f'{id = }')
    # return render(request, 'app/articles_detail.html')
    return render(request, 'app/05_urls.html', {'id': id})

def articles_category(request, category, id):
    print(f'{ category = }, {id = }')
    # return render(request, 'app/articles_category.html')
    return render(request, 'app/05_urls.html', { 'id' : id, 'category' : category })

def search(request):
    print(request.GET.urlencode())
    print(request.GET)
    # q = request.GET.get('q', '')
    q = request.GET.getlist('q', '')
    lang = request.GET.get('lang', '')
    print(f'{ q = }, { lang = }')
    return render(request, 'app/05_urls.html', { 'q': q, 'lang' : lang})
