
"""
介绍__call__方法的作用
class Person(object):

    def dadoudou(self):
        print("打豆豆")
    
    # 如果希望对象能够被调用就需要实现__call__ 方法
    def __call__(self, *args, **kwargs):
        print("打豆豆")

p = Person()

p()  # 'Person' object is not callable  函数和方法才能够被调用


# p.dadoudou()

"""


class Person(object):
    def __init__(self, func_ref):
        self.func = func_ref


    def __call__(self, *args, **kwargs):
        self.func()


@Person  # dadoudou = Person(dadoudou)  --> dadoudou 实际上是一个Person类型的实例对象
def dadoudou():
    print("打豆豆")

# 调用实例对象   'Person' object is not callable
dadoudou()  # 实际上调用的是Person类型的对象的__call__方法




