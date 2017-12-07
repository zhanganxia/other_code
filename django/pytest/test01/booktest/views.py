from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("index")
    context={'title':'哈哈','list':range(10)}
    return render(request,'booktest/index.html',context)