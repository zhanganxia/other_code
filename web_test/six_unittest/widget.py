#coding=utf-8

#将要被测试的类
class Widget:
    def __init__(self, size=(40,40)):#self代表类本身
        self._size = size  #self.size是私有的不能被类以外的函数和方法调用
    def getSize(self):#赋值函数getXX和取值函数setXXX
        return self._size
    def resize(self,width,height):
        if width<0 or height<0:
            raise ValueError,"illegal size"
        self._size = (width,height)
    def dispose(self):
        pass
        __init__()

    #python中没有显示的private和public限定符，如果要将一个方法声明为private的，只要在方法名前加上“——”即可