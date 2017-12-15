from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import PicTest,AreaInfo


# Create your views here.
def jingtai(request):
    return render(request,'booktest/jingtai.html')
    
def pic_upload(request):
    '''上传图片'''
    return render(request,'booktest/pic_upload.html')

def pic_handle(request):
    '''接收并保存图片'''
    f1 = request.FILES.get('pic')
    fname = '%s/booktest/%s'%(settings.MEDIA_ROOT,f1.name)
    print(fname)
    with open(fname,'wb') as pic:
        for c in f1.chunks():
            pic.write(c)

    return HttpResponse('OK')

def pic_show(request):
    pic=PicTest.objects.get(pk=1)
    context={'pic':pic}
    return render(request,'booktest/pic_show.html',context)

def pagelist(request,pindex):
    '''实现省的分页功能'''
    sheng=AreaInfo.objects.filter(aParent__isnull=True)
    paginator = Paginator(sheng,10)
    if pindex =='':
        pindex= '1'
    page=paginator.page(int(pindex))
    return render(request,'booktest/page_test.html',{'page':page})

def area_select(request):
    return render(request,'booktest/area_select.html')


