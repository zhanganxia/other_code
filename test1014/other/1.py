#!/bin/env python2
# class Singleton(type): 
#     def __init__(self,name,bases,dict): 
#         # super(Singleton,self).__init__(name,bases,dict)
#         self.instance=None
     
#     def __call__(self,*args,**kw):
#         if self.instance is None: 
#             self.instance=super(Singleton,self).__call__(*args,**kw)
#             return self.instance

# class MyClass(object):
#     __metaclass__ = Singleton
#     # vc = "ccc"

# # class MyClass2(object):
# #     __metaclass__ = Singleton

# print MyClass()
# # print MyClass2()
# # print MyClass2()

# print MyClass()



def singleton(cls):
    instances={}
    def getinstance(): 
        if cls not in instances:
            instances[cls]=cls()
            return instances[cls]
        return getinstance

@singleton
class MyClass:
    xxxx