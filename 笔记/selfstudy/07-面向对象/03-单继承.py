class Dog(object):
    def __init__(self,name,color= "白色"):
        self.name = name
        self.color = color
    
    def run(self):
        print("%s-->在跑"%self.name)

class Hasq(Dog):
    def setName(self,name):
        self.setName = name
    def eat(self):
        print("%s-->在吃东西"%self.name)

hs = Hasq("哈士奇")
print('hs的名字为：%s'%hs.name)
print('hs的颜色为：%s'%hs.color)

hs.eat()
hs.setName('金毛')
hs.run()



