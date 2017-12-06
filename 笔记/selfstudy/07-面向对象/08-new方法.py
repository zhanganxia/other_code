class A(object):
    def __init__(self):
        print('*****',self)
        print("-----这是init方法---")

    def __new__(cls):
        print(id(cls),'########')
        print("这是new方法******")
        ret = object.__new__(cls)
        print('22222222',ret)
        return ret

# 94878931982648 ########
# 这是new方法******
# 22222222 <__main__.A object at 0x7f5303bb5908>
# ***** <__main__.A object at 0x7f5303bb5908>
# -----这是init方法---

A()
# 总结：
# 1.__new__的调用优先于__init__
# 2.继承自object的新式类才有__new__
# 3.__init__有一个参数self,就是这个__new__返回的实例，
#   __init__在__new__的基础上可以完成一些其他的初始化的动作，
#   __init__没有返回值
# 4.__new__的cls参数指代的是：实例化的那个类(A)，这个参数在实例化时由Python解释器自动提供
# 5.__new__必须要有返回值，返回实例化出来的实例
        