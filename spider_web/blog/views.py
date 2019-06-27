from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def indexOld(request):
    return HttpResponse('welcome to visit tr')


def index(request):
    return render(request, 'blog/index.html', context={
        'title': 'tr blog',
        'welcome': 'welcome to visit tr',
    })
