from django.contrib import admin

from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner,GoodsSKU,Goods


class GoodsSpuAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class GoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['id','sku']

admin.site.register(Goods,GoodsSpuAdmin) #商品SPU df_goods
admin.site.register(GoodsType) #商品分类df_goods_type
admin.site.register(GoodsSKU) #商品SKU df_goods_sku
admin.site.register(IndexGoodsBanner,GoodsBannerAdmin) #商品轮播图df_index_banner
admin.site.register(IndexPromotionBanner) #促销商品信息df_index_promotion
admin.site.register(IndexTypeGoodsBanner) #首页分类商品展示信息df_index_type_goods



