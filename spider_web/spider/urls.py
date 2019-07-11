from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^fetch$', views.fetch, name='fetch'),
    url(r'^getThreadInfo$', views.getThreadInfo, name='getThreadInfo'),
]
