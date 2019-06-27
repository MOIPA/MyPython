import threading
from django.shortcuts import render
from django.http import HttpResponse
from spider.spiderPy.fetchByKeyWord import startSpider

# Create your views here.


def thread(arg1, arg2, arg3, arg4):
    startSpider(arg1, arg2, arg3, arg4)


def fetch(request):
    type = request.GET.get('type')
    theme = request.GET.get('theme')
    date = request.GET.get('date')
    module_id = request.GET.get('module_id')
    # spider_thread = threading.Thread(target=thread, args=('食品安全', '牛奶', 1, 1,))
    spider_thread = threading.Thread(target=thread,
                                     args=(type, theme, date, module_id))
    spider_thread.start()
    # startSpider('食品安全', '牛奶', 1, 1)

    return HttpResponse(0)
