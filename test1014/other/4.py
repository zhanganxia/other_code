#encoding:utf-8
class Animal(object):
    def eye(self):
        print "我有眼睛"
# 大类:
class Mammal(Animal):
    def shengwa(self):
        "dddd"
        print "我可以生娃"

class Bird(Animal):
    def fly(self):
        "dddd"
        print "我可以飞"

# 各种动物:
class Dog(Mammal):
    def yao(self):
        "dddd"
        print "我可以咬人"


class JenMAo(Dog):
    def jm_cc(self):
        "金毛方法"
        print "我是金毛"


jm1 = JenMAo()


jm1.eye()
jm1.shengwa()
jm1.yao()
jm1.jm_cc()