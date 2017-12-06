#定义一个类
class Animal:
    #方法
    def __init__(self,name):
        self.name = name
        print("1")

    def printName(self):
        print('名字为：%s'%self.name)
        print("2")

#定义一个函数
def myPrint(animal):
    animal.printName()
    print("3")

dog1 = Animal("xixi")
myPrint(dog1)
print("4")

dog2 = Animal("baby")
myPrint(dog2)
print("5")







