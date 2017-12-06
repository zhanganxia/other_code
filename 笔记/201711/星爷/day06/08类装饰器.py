#类不能被直接调用，函数方法才能被调用，如果要调用类，要在类中定义__call__方法

# class person(object):
#     def __init__(self):        
#         self.name = "丫丫"
#         self.age = 15
#         print("My name is %s,i‘m %d years old!"%(self.name,int(self.age)))
#     def __call__(self,*args,**kwargs):
#         print("I am a human!")

# person = person()
# person()    

class Person(object):
    def __init__(self,func_ref):        
        self.func = func_ref
        
    def __call__(self,*args,**kwargs):
        self.func()

@Person
def msg():   
    name = "丫丫"
    age = 18
    print("My name is %s,i‘m %d years old!"%(name,int(age)))

msg()
# person = person()
# person() 

