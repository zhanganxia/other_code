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
        sku_ids = ','.join(sku_ids) #把列表转换成一个以逗号分隔的字符串
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

# 订单的创建的流程：
# 接收参数
# 参数校验
# 组织订单信息
# todo:向df_order_info表中添加一条记录

# todo:遍历向df_order_goods中添加记录
# 获取商品的信息
# 从redis中获取用户要购买商品的数量
# todo：减少商品的库存，增加销量
# todo:累加计算用户要购买的商品的数目和总价格

# todo: 更新order对应记录中的total_count和total_price
# 注意：(为了防止篡改信息，所以总数目和总价格需要重新计算，而不是从上一个页面传递过来)
# todo: 删除购物车中对应的记录
# todo: 删除购物车中对应的记录

# 返回应答

# /order/commit
# 前端采用ajax post请求
# 传递的参数：收货地址id(addr_id) 支付方式(pay_method) 用户要购买商品的id(sku_ids)1,2,3
class OrderCommitView(View):
    '''订单创建'''
    def post(self,request):
        '''订单创建'''
        pass