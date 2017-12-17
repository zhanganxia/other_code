from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# 创建session_set和session_get视图如下（测试redis存储session）
def session_set(request):
    request.session['name'] = 'zax'
    return HttpResponse('ok')

def session_get(request):
    name = request.session['name']
    return HttpResponse(name)

