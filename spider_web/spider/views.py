import threading
from django.shortcuts import render
from django.http import HttpResponse
from spider.spiderPy.fetchByKeyWord import startSpider

# Create your views here.


def thread(arg1, arg2, arg3, arg4, arg5):
    startSpider(arg1, arg2, arg3, arg4, arg5)


def fetch(request):
    type = request.GET.get('type')
    theme = request.GET.get('theme')
    date = request.GET.get('date')
    model_id = request.GET.get('model_id')
    drop = request.GET.get('drop')
    # spider_thread = threading.Thread(target=thread, args=('食品安全', '牛奶', 1, 1,))
    spider_thread = threading.Thread(target=thread,
                                     args=(type, theme, date, model_id, drop,))
    spider_thread.start()
    # startSpider('食品安全', '牛奶', 1, 1)

    return HttpResponse(0)
