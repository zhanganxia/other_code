class Singleton(object):
    instance = None

    def __new__(cls,age,name):
        if not cls.instance:
            cls.instance = object.__new__(cls)
        return cls.instance

a = Singleton(23,"zax")
b = Singleton(24,"ljq")

a.age = 18
print("b的年龄是：",b.age)
    