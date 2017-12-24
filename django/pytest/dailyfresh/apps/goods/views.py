from django.shortcuts import render
from django.views.generic import View
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner

# http://127.0.0.1:8000
class IndexView(View):
    def get(self,request):
        '''首页显示'''
        # 获取商品分类信息
        types = GoodsType.objects.all()
        
        # 获取首页轮播商品的信息
        goods_banner = IndexGoodsBanner.objects.all().order_by('index')

        # 获取首页促销活动的信息
        promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

        # 获取首页分类商品展示信息
        # types_goods_banner = IndexTypeGoodsBanner.objects.all().order_by('index')
        for type in types:
            # 根据type查询type种类首页展示的文字商品信息和图片商品信息
            title_banner = IndexTypeGoodsBanner.objects.filter(type=type,display_type=0).order_by('index')
            image_banner = IndexTypeGoodsBanner.objects.filter(type=type,display_type=1).order_by('index')
            # 给type对象增加两个属性title_banner和image_banner
            # 分别保存type种类首页展示的文字商品信息和图片商品信息
            type.title_banner = title_banner
            type.image_banner = image_banner

        # 获取用户购物车商品的数目
        cart_count = 0

        # 组织上下文
        context = {
            'types':types,
            'goods_banner':goods_banner,
            'promotion_banner':promotion_banner,
            # 'types_goods_banner':types_goods_banner,
            'cart_count':cart_count
        }

        # 使用模板
        return render(request,'index.html',context)
