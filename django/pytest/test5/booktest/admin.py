from django.contrib import admin
from booktest.models import AreaInfo,PicTest
# Register your models here.

# class AreaStackedInline(admin.StackedInline):
#     model = AreaInfo #关联子对象
#     extra = 2 # 额外编辑2个子对象

class AreaTabularInline(admin.TabularInline):
    model = AreaInfo 
    extra = 2

class AreaAdmin(admin.ModelAdmin):
    list_per_page = 10
    # fields = ['aParent','atitle']

    actions_on_top = True
    actions_on_bottom = True

    # 列表中的列：list_display=[模型字段1，模型字段2，...]
    # 点击列头可以进行升序或降序排列
    # list_display = ['id','atitle']
    list_display = ['id','atitle','title','parent']

    # 分组显示
    fieldsets = (
        ('基本',{'fields':['atitle']}),
        ('高级',{'fields':['aParent']})
    )
    
    # inlines = [AreaStackedInline]
    inlines = [AreaTabularInline]

    # list_filter=[]会将对应字段的值列出来
    list_filter = ['atitle']

    # search_field=[]用于对指定字段的值进行搜索，支持模糊查询
    search_fields = ['atitle']

admin.site.register(AreaInfo,AreaAdmin)

# 注册admin页面
admin.site.register(PicTest)