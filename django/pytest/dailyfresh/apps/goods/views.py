from django.shortcuts import render

# http://127.0.0.1:8000
def index(request):
    '''首页'''
    return render(request,'index.html')
