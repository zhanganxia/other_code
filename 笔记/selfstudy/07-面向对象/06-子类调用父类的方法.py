class Dog(object):
    def __init__(self,name):
        self.name = name
        self.sound = "汪汪"

class Jm(Dog):
    def __init__(self,name):
        super().__init__(name)
        #super().sound
        print("my name is %s,my sound is %s"%(self.name,self.sound))

    def getName(self):
        return self.name

jin_m = Jm("金毛")

print(jin_m.name)
print(jin_m.sound)

