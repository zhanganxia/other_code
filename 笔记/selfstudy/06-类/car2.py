#定义__str__()方法
#encoding=utf-8
class Car:
    def __init__(self,newWheelNum,newColor):
        self.wheelNum = newWheelNum
        self.color = newColor

    def __str__(self):
        msg = "我的颜色是：" + self.color+"我有" + int(self.wheelNum) + "个轮子"
        return msg

    def move(self):
        print("我在移动")

BW = Car(4,"白色")
print(BW)
