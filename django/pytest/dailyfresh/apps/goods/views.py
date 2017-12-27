from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from goods.models import GoodsSKU,GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from order.models import OrderGoods
from django_redis import get_redis_connection
from django.core.cache import cache
from django.core.paginator import Paginator

# http://127.0.0.1:8000
class IndexView(View):
    def get(self,request):
        '''首页显示'''
        # 先尝试从缓存中获取数据
        context = cache.get('index_page_data')

        if context is None:
            print('设置首页数据缓存')
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

            # 组织缓存的数据
            context = {
                'types':types,
                'goods_banner':goods_banner,
                'promotion_banner':promotion_banner,
                'cart_count':cart_count
            }

            # 设置缓存 pickle
            # 缓存api的使用
            # from django.core.cache import cache
            # cache.set(缓存名称，缓存内容，有效时间)：设置缓存
            # cache.get(缓存名称)：获取缓存
            # cache.delete(缓存名称)：删除缓存
            cache.set('index_page_data',context,3600)
        cart_count = 0
        # 获取user的登录状态
        user = request.user
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context.update(cart_count=cart_count)

        # 使用模板
        return render(request,'index.html',context)

# 访问商品的详情页面时，需要传递商品的id
# 前端向后端传递参数的额方式：
    # 1. get(只涉及到数据的获取) /goods?sku_id = 商品id
    # 2. post(涉及到数据的修改)传递
    # 3. url捕获参数 /goods/商品id
class DetailView(View):
    '''商品详情页面'''
    def get(self,request,sku_id):
        # 获取sku_id商品的详情信息
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoseNotExist:
            # 商品不存在，跳转到首页
            return redirect(reverse('goods:index'))
        # 获取商品的分类信息
        types = GoodsType.objects.all()
        # 获取和商品同一分类的2个商品信息
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]
        # 获取商品的评论信息
        order_sku = OrderGoods.objects.filter(sku=sku).exclude(commont='').order_by('-update_time')
        
        # 获取和sku商品同一SPU的其他规格的商品
        same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=sku_id)
        # 获取登录用户的额购物车中商品的条目信息
        cart_count = 0
        user = request.user
        if user.is_authenticated():
            # 用户已登录，获取用户购物车中商品的条目数
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

            # 添加用户历史浏览记录
            history_key = 'history_%d'%user.id
            # 先尝试从redis对应的列表删除元素sku_id
            conn.lrem(history_key,0,sku_id)
            # 把sku_id加入到redis对应列表的左侧
            conn.lpush(history_key,sku_id)
            # 保留用户最近浏览的5个商品的浏览记录:ltrim
            conn.ltrim(history_key,0,4)
        # 组织模板上下文
        context = {
            'sku':sku,
            'types':types,
            'new_skus':new_skus,
            'order_sku':order_sku,
            'cart_count':cart_count,
            'same_spu_skus':same_spu_skus
        }

        # 使用模板
        return render(request,'detail.html',context)

#访问列表页面需要传递的参数
# 种类id(type_id),页码(page)，排序方式(sort)
# /list?type_id=种类id&page=页码&sort=排序方式
# /list/种类id/页码/排序方式
# /list/种类id/页码?sort=排序方式
class ListView(View):
    '''列表页面'''
    def get(self,request,type_id,page):
        '''显示'''
        # 获取type_id对应的分类信息
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            # 商品种类不存在，跳转到首页
            return redirect(reverse('goods:index'))
        print('******',type)
        # 获取商品分类信息
        types = GoodsType.objects.all()

        # 获取排序方式 获取分类商品的信息 
        sort = request.GET.get('sort','default')
        # sort=='default':按照默认方式(商品id)排序
        # sort=='price':按照商品的价格(price)排序
        # sort== 'hot':按照产品的销量(sales)排序
        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'hot':
            skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            # 默认排序
            sort = 'default'
            skus = GoodsSKU.objects.filter(type=type).order_by('-id')
        
        # 分页
        paginator = Paginator(skus,1)
        # 处理页码
        page = int(page)
        if page > paginator.num_pages or page <= 0:
            # 默认显示第一页
            page = 1
        # 获取第page页的Page对象
        skus_page = paginator.page(page)

        # 页码处理（页面最多值显示出5个页码）
        # 1.总页数不是5页，显示所有页码
        # 2.当前页是前3页，显示1-5页
        # 3.当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1,num_pages+1)
        elif page <=3:
            pages = range(1,6)
        elif num_pages - page <=2:
            pages = range(num_pages-4,num_pages+1)
        else:
            pages = range(page-2,page+3)

        # 获取分类的两个新品信息
        new_skus = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]
        # 获取登录用户购物车中商品的条目数
        cart_count = 0
        user = request.user
        if user.is_authenticated():
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)
        # 组织模板上下文
        context = {
            'type':type,
            'types':types,
            'skus':skus,
            'skus_page':skus_page,
            'new_skus':new_skus,
            'cart_count':cart_count,
            'sort':sort,
            'pages':pages
        }
        # 使用模板
        return render(request,'list.tmpl',context)
