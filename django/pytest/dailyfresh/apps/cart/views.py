from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from goods.models import GoodsSKU
from django_redis import get_redis_connection

# 前端采用ajax post请求
# 需要传递的参数：商品id(sku_id) 商品数目（count）
class CartAddView(View):
    '''购物车记录添加'''
    def post(self,request):
        '''记录添加'''
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res':0,'errmsg':'用户未登录'})

        # 接收参数
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 参数校验
        if not all(sku_id,count):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})
        # 校验商品id
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except Exception as e:
            # 商品数目非法
            return JsonResponse({'res':3,'errmsg':'商品数目非法'})
        
        if count <= 0:
            # 商品数目非法
            return JsonResponse({'res':4,'errmsg':'商品数量不合法'})
        # 业务处理，购物车添加

        # 如果用户购物车中已经添加过该商品，需要进行数目累加（从redis中获取）
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # 先尝试从cart_key对应的hash元素中获取属性sku_id的值
        cart_count = conn.hget(cart_key,sku_id)
        if cart_count:
            # 用户购物车中已经添加过该商品，数目需要累加
            count += int(cart_count)

        # 判断商品的库存
        if count>sku.stock:
            return JsonResponse({ 'res':5,'errmsg':'商品库存不足' })

        # 设置用户购物车中商品的数目
        conn.hset(cart_key,sku_id,count)
        # 返回应答
        return JsonResponse({ 'res':6,'message':'添加记录成功' })
