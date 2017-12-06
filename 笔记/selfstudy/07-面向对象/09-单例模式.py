# 单例模式
# 确保某一个类只有一个实例，而且自行实例化并向整个系统提供这个实例，这个类称为
# 单例类，单例模式是一种对象创建型模式

class Singleton(object):
    __instance = None
    
    def __new__(cls,name,age):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            print('******',cls.__instance)
            print('name',name)
            print('age',age)
        return cls.__instance
    

a = Singleton(18,"zax")
b = Singleton(20,"ljq")

print(id(a))
print(id(b))


a.age = 22
print(b.age)


#单例模式的目的:令单个进程中只有一个类的实例,从而可以实现数据的共享,节省系统开销,防止io阻塞等等 