#coding=utf-8
name = "李坚强"

class Student():
    def __init__(self):
        self.name = "zax"
        self.__age = 20

    def SetAge(self,age):
        self.__age = age

    def GetAge(self):
        return self.__age

    def SetName(self,name):
        name = "张安侠"
        self.name = name


print name
jan1 = Student()
print jan1.name
# jan1.SetName(name)
print jan1.name


jan1.name 
jan1.name = "cccc"

# print jan1.GetAge()