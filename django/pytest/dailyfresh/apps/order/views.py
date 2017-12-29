from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods
from django_redis import get_redis_connection


# /order/
# request.GET request.POST -->QueryDict
# 允许一个名字对应多个值 getlis()
class OrderView(LoginRequiredMixin,View):
    '''提交订单页面显示'''
    def post(self,request):
        '''显示'''
        # 获取用户所要购买的商品的id
        sku_ids = request.POST.getlist('sku_id')
        print('^^^^',sku_ids)
        # 数据校验
        if not all([sku_ids]):
            return redirect(reverse('cart:show'))
        # 业务处理:页面信息的获取(用户收货地址信息)
        user = request.user
        addrs = Address.objects.filter(user=user)
        # 获取用户购买的商品信息(cart_key,skus(商品信息),total_count,total_price)
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        skus = []
        total_count = 0
        total_price = 0
        
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)
            # 获取用户所要购买的商品的数量
            count = conn.hget(cart_key,sku_id)
            # 计算商品的小计
            amount =  sku.price * int(count)
            # 给sku增加属性count和amount，分别保存用户所要购买的商品的数目和小计
            sku.count = count
            sku.amount = amount
            # 添加商品
            skus.append(sku)

            # 累加计算用户要购买的商品的总数目和总金额
            total_count += int(count)
            total_price +=  amount

        # 运费:运费的子系统
        transit_price = 10
        # 实付款
        total_pay = total_price + transit_price
        # 组织上上下文
        sku_ids = ','.join(sku_ids)
        context={
            'total_count':total_count,
            'total_price':total_price,
            'transit_price':transit_price,
            'total_pay':total_pay,
            'addrs':addrs,
            'skus':skus,
            'sku_ids':sku_ids
        }
        # 使用模板

        return render(request, 'place_order.html', context)

