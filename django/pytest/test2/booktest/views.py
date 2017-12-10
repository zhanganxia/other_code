from django.shortcuts import render
from django.http import HttpResponse
from booktest.models import BookInfo,HeroInfo
from django.db.models import F,Q,Sum,Count
from booktest.models import AreaInfo


def index(request):
    str='%s<br>%s'%(request.path,request.encoding)
    return HttpResponse(str)

# def index1(request,value1,value2):
#     context = {'v1':value1,'v2':value2}
#     return render(request,'booktest/index.html',context)

def index2(request,parameter1,parameter2):
    context1 = {'val01':parameter1,'val02':parameter2}
    return render(request, 'booktest/index.html',context1)

def method1(request):
    return render(request,'booktest/method1.html')

def method2(request):
    return HttpResponse(request.method)

def method3(request):
    return HttpResponse(request.method)

def get(request):
    # 通过GET属性获取地址栏上的数据，获取的QueryDict对象
    dict = request.GET

    a = dict.getlist('a') #返回所有值
    b = dict.get('b')

    context = {'a':a, 'b':b}
    return render(request,'booktest/get.html',context)

def getwish(request):
    dict = request.GET
    name = dict.get('name')
    list = dict.getlist('a')
    textlist = ['生日快乐','节日快乐','学习进步','四季平安']
    str = ''
    for i in list:
        str += textlist[int(i)]+ ' '
    context = {'name':name,'wish' : str}
    return render(request,'booktest/getwish.html',context)

def booklist(request):
    # 1.获取所有图书
    books1 = BookInfo.objects.all()
    books1 = BookInfo.objects.shuminghao(books1)
    # 2.查询所有未逻辑删除的数据
    books2 = BookInfo.objects.total()
    # 3.查询id==1的数据
    books3 = BookInfo.objects.filter(id__exact=1) #等价于filter(id=1)
    # 4.模糊查询书名包含'传'的数据
    books4 = BookInfo.objects.filter(btitle__contains='传')
    # 5.模糊查询书名以”湖“结尾的书名
    books5 = BookInfo.objects.filter(btitle__endswith='湖')
    # 6.查询备注不为空的图书数据
    books6 = BookInfo.objects.filter(bcontext__isnull=False)
    # 7.范围查询，查询图书编号为1，3的数据
    books7 = BookInfo.objects.filter(id__in=[1,3])
    # 8.查询图书编号大于3的数据
    books8 = BookInfo.objects.filter(id__gt=3)
    # 9.查询发布日期为1986年的图书
    books9 = BookInfo.objects.filter(bpub_date__year=1986)
    # 10.查询id!=3的图书信息
    books10 = BookInfo.objects.exclude(id=3)
    # 11.查询阅读量大于等于评论量的图书信息
    books11 = BookInfo.objects.filter(bread__gte=F('bcommet'))
    # 12.查询id大于3且阅读量大于30的图书信息
    books12 = BookInfo.objects.filter(Q(id__gt=3)&Q(bread__gt=30))
    # 13.查询所有图书从大到小排列
    books13 = BookInfo.objects.all().order_by('-id')
    # 14.把id大于1的图书信息按阅读量从大到小排序显示
    books14 = BookInfo.objects.filter(id__gt=1).order_by('-bread')
    # 15.查询所有图书阅读量的总和
    books15 = BookInfo.objects.aggregate(Sum('bread'))['bread__sum']
    # 16.查询图书，要求图书中英雄的描述包含'十'
    books16 = BookInfo.objects.filter(heroinfo__hcontent__contains='十')
    # 17.
    

    context = {
        'books1':books1,
        'books2':books2,
        'books3':books3,
        'books4':books4,
        'books5':books5,
        'books6':books6,
        'books7':books7,
        'books8':books8,
        'books9':books9,
        'books10':books10,
        'books11':books11,
        'books12':books12,
        'books13':books13,
        'books14':books14,
        'books15':books15,
        'books16':books16
        }
    return render(request,'booktest/booklist.html',context)

def area(request):
    area = AreaInfo.objects.get(atitle='广州市')
    return render(request,"booktest/area.html",{'area':area})