from django.contrib import admin

from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner,GoodsSKU,Goods


class BaseAdmin(admin.ModelAdmin):
    '''新增或者更新数据时被调用'''
    def save_model(self, request, obj, form, change):
        # 调用父类的方法，完成新增或者更新的操作
        super().save_model(request, obj, form, change)
        # 附加操作，发出generate_static_index_html任务
        from celery_tasks.sendmail_task import generate_static_index_html
        generate_static_index_html.delay()
        print('send generate_static_index_html ok')

    def delete_model(self, request, obj):
        # 调用父类的方法，完成删除的操作
        super().delete_model(request,obj)
        # 附加操作，发出generate_static_index_html任务
        from celery_tasks.sendmail_task import generate_static_index_html
        generate_static_index_html.delay()

class GoodsTypeAdmin(BaseAdmin):
    pass

class GoodsSpuAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class GoodsBannerAdmin(BaseAdmin):
    list_display = ['id','sku']

class IndexPromotionBannerAdmin(BaseAdmin):
    pass

class IndexTypeGoodsBannerAdmin(BaseAdmin):
    pass

admin.site.register(Goods,GoodsSpuAdmin) #商品SPU df_goods
admin.site.register(GoodsType,GoodsTypeAdmin) #商品分类df_goods_type
admin.site.register(GoodsSKU) #商品SKU df_goods_sku
admin.site.register(IndexGoodsBanner,GoodsBannerAdmin) #商品轮播图df_index_banner
admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin) #促销商品信息df_index_promotion
admin.site.register(IndexTypeGoodsBanner,IndexTypeGoodsBannerAdmin) #首页分类商品展示信息df_index_type_goods



