class People(object):
    def __init__(self,name):
        self.__name = name

    def getName(self):
        print("+++++",self.__name)
        return self.__name

    def setName(self,newName):
        if len(newName) >= 5:
            self.__name = newName
            print("-----",self.__name)
        else:
            print("error:名字长度需要大于或者等于5")

xiaoming = People("dongGe")
#print(xiaoming.__name)

#setName -->将名字信息传递给类属性
#getName -->获取类属性中的名字信息
xiaoming.setName("wanger")
print(xiaoming.getName())

xiaoming.setName("zhanganxia")
print(xiaoming.getName())






