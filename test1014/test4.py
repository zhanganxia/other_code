#encoding=utf-8
import string

class A:
    count = 0
class B(A):
    def __init__(self):
        A.count += 1
    def __del__(self):
        A.count -= 1
if __name__=='__main__':
    a1 = B()
    b2 = B()
    print("B 对象实例数:" B.count)
    del(b2)
    print("B 对象实例数:" B.count)