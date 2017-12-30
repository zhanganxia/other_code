from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods
from django_redis import get_redis_connection
from datetime import datetime
from django.db import transaction


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
    @transaction.atomic
    def post(self,request):
        '''订单创建'''
        user =  request.user
        if not user.is_authenticated():
            return JsonResponse({'res':0,'errmsg':'用户未登录'})
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')

        # 参数校验
        if not all([addr_id,pay_method,sku_ids]):
            return JsonResponse({'res':1,'errmsg':'参数不完整'})

        # 校验地址信息
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            # 地址不存在
            return JsonResponse({'res':2,'errmsg':'地址信息错误'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            # 支付方式非法
            return JsonResponse({'res':3,'errmsg':'支付方式非法'})
        # 组织订单信息
        # 订单id:20171226120029+用户id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        # 运费
        transit_price = 10
        # 总数目和总价格
        total_count = 0
        total_price = 0

        # todo:设置事务保存点
        sid = transaction.savepoint()

        try:
            # todo:向df_order_info表中添加一条记录
            order = OrderInfo.objects.create(order_id=order_id,user=user,addr=addr,pay_method=pay_method,
                                    total_count=total_count,total_price=total_price,transit_price=transit_price)

            # todo:遍历向df_order_goods中添加记录
            conn =  get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            sku_ids = sku_ids.split(',')
            for sku_id in sku_ids:
                # 获取商品的信息
                try:
                    sku = GoodsSKU.objects.get(id=sku_id)
                except GoodsSKU.DoesNotExist:
                    # 商品不存在，回滚到sid事务保存点
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'res':4,'errmsg':'商品不存在'})

                # 获取用户要购买的商品的数量（从redis中读取）
                count = conn.hget(cart_key,sku_id)
                print('^^^^',sku.stock)
                # 判断商品的库存
                if int(count) > sku.stock:
                    # 商品库存不足，回滚到事务保存点
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'res':6,'errmsg':'商品库存不足'})

                # todo:向df_order_goods中添加一条记录
                OrderGoods.objects.create(order=order,sku=sku,count=count,price=sku.price)

                # todo:减少商品的库存，增加销量
                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()

                 # todo:累加计算用户要购买的商品的总数目和总价格
                total_count += int(count)
                total_price += sku.price*int(count)

            # todo:更新order对应记录中的total_count和total_price
            order.total_count = total_count
            order.total_price = total_price
            order.save()

        except Exception as e:
            # 数据库出错，回滚到事务保存点
            transaction.savepoint_rollback(sid)
            return JsonResponse({'res':7,'errmsg':'下单失败'})

           
        # todo:删除购物车中对应的记录 sku_ids=[1,2],*sku_ids相当于解包，将每个元素做为参数
        conn.hdel(cart_key,*sku_ids)

        # 返回应答
        return JsonResponse({'res':5,'message':'订单创建成功'})