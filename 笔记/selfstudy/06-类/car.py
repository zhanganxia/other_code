#定义类
class Car:
    #移动
    def move(self):
        print("车在奔跑...")
    #鸣笛
    def toot(self):
        print("车在鸣笛.........")

#创建一个对象，并用变量BM来保存它的引用
BM = Car()
BM.color = '黑色'
BM.wheelNum = 4#轮子数量
BM.move()
BM.toot()
print(BM.color)
print(BM.wheelNum)

