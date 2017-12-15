from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from booktest.models import PicTest,AreaInfo


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
    '''省市区下拉框选择页面'''
    return render(request,'booktest/area.html')


def areas(request):
    '''处理页面ajax请求'''
    parent = request.GET.get('parent')
    # print(parent)
    if parent == 'None':
        areas = AreaInfo.objects.filter(aParent_id = None)
        # print(areas)
    else:
        areas = AreaInfo.objects.filter(aParent_id = parent)
        print('*',areas)

    jsonstr = []
    for area in areas:
        jsonstr.append({'id':area.id,'atitle':area.atitle,'aparent':area.aParent_id})

    print('--',jsonstr)
    return JsonResponse({'data':jsonstr})
