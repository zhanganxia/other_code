#coding=utf-8
class baseObj(object):
    def test(self):
        print("------base test--------")

class A(baseObj):
    def printA(self):
        print("-------A-------")

class B(baseObj):
    def printA(self):
        print('-------B-------')

class C(B,A):
    def printC(self):
        print('-------C--------')

obj_C = C()
obj_C.printA()
obj_C.printA()

obj_C.test()
print(C.__mro__)
