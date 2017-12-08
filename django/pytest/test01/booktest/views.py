from django.shortcuts import render
from django.http import HttpResponse
from booktest.models import BookInfo,HeroInfo 

# 展示所有图书
def index(request):
    # 查询所有图书
    booklist = BookInfo.objects.all()
    # 将图书列表传递到模板中，然后渲染模板
    return render(request,'booktest/index.html',{'booklist':booklist})

# 书籍详情显示
def detail(request,id):
    # 根据图书编号查找对应的图书
    book = BookInfo.objects.get(pk=id)
    # 将图书信息放入模板进行渲染
    return render(request,'booktest/detail.html',{'book':book})