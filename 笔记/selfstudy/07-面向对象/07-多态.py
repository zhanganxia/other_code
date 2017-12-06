class F(object):
    def show(self):
        print("F1.show")

class S1(F):
    def show(self):
        print("S1.show")

class S2(F):
    def show(self):
        print("S2.show")

def Func(F, obj):
    print(obj.show())

# s1_obj = S1()
# Func(s1_obj)

s2_obj = S2()
Func(s2_obj)