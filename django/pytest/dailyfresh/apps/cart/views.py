from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin

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
        count = int(request.POST.get('count'))
        
        # 参数校验
        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})
        # 校验商品id
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except Exception as e:
            # 商品数目非法
            return JsonResponse({'res':3,'errmsg':'商品信息错误'})
        # 校验商品的数目
        try:
            count = count
        except Exception as e:
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
        if count > sku.stock:
            return JsonResponse({ 'res':5,'errmsg':'商品库存不足' })

        # 设置用户购物车中商品的数目
        conn.hset(cart_key,sku_id,count)

        # 获取用户购物车中商品的条目数
        cart_count = conn.hlen(cart_key)
        print('******',cart_count)
        # 返回应答
        return JsonResponse({ 'res':6,'cart_count':cart_count,'message':'添加记录成功' })

# /cart/
class CartInfoView(LoginRequiredMixin,View):
    '''购物车页面显示'''
    def get(self,request):
        '''显示'''
        # 获取登录的用户
        user = request.user

        # 获取用户购物车中的记录信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        cart_dict = conn.hgetall(cart_key) #{商品id：商品数量}
        print('********',cart_dict)

        skus = []
        total_count = 0
        total_price = 0
        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            print('#############',sku_id)
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price*int(count)
            # 给sku增加属性count,amount,分别保存用户购物车中添加的商品的数目和商品的小计
            sku.count = count
            sku.amount = amount
            # 添加商品
            skus.append(sku)

            # 累加计算用户购物车中商品的总数目的总价格
            total_count += int(count)
            total_price += amount

            # 组织模板上下文
            context = {
                'total_count':total_count,
                'total_price':total_price,
                'skus':skus
            }

        # 使用模板
        return render(request,'cart.html',context)


# /cart/update
#前端采用ajax post请求
class CartUpdateView(View):
    def post(self,request):
        '''更新'''
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res':0,'errmsg':'用户未登录'})
        # 接收参数
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 参数校验
         # 参数校验
        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})
        # 校验商品id是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except Exception as e:
            # 商品数目非法
            return JsonResponse({'res':3,'errmsg':'商品信息错误'})
        # 校验商品的数目是否合法
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res':4,'errmsg':'商品的数目不合法'})

        if count <= 0:
            return JsonResponse({'res':5,'errmsg':'商品的数目不合法'})

        # 业务处理：购物车记录的更新
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id

        # 判断商品的数目是否大于商品的库存:
        if count > sku.stock:
            return JsonResponse({'res':5,'errmsg':'商品库存不足'})

        #更新redis中的记录
        conn.hset(cart_key,sku_id,count)

        return JsonResponse({'res':6,'errmsg':'信息更新成功'})