#示例属性
#cookedLevel:0~3-->生的 ；3~4 ：半生 5~8：熟了；>8：焦了
#cookedString:字符串，描述地瓜的生熟程度
#condiments:这是地瓜的配料列表

#定义地瓜类
class SweetPotato:
    '这是烤地瓜的类'
    #定义初始化方法
    def __init__(self):
        self.cookedLevel = 0
        self.cookedString = "生的"
        self.condiments = []

    #定制print显示的方法
    def __str__(self):
        msg = self.cookedString + "地瓜"
        if len(self.condiments)>0:            
            msg = msg + "("
            for temp in self.condiments:
                msg = msg + temp +","
            msg = msg + ")"
        return msg                 
    def addCondiments(self,condiments):
        self.condiments.append(condiments)      

    #定义烤地瓜方法
    def cook(self,time):
        self.cookedLevel += time
        if self.cookedLevel > 8:
            self.cookedString = "焦了"
        elif self.cookedLevel >5:
            self.cookedString = "熟了"
        elif self.cookedLevel >3:
            self.cookedString = "半生"
        elif self.cookedLevel >0:
            self.cookedString = "生的"
#创建对象
mySweetPotato = SweetPotato()
print("有一个地瓜还没烤")
print(mySweetPotato.cookedLevel)
print(mySweetPotato.cookedString)
print(mySweetPotato.condiments)

print("------烤地瓜--------")
print("烤4分钟")
mySweetPotato.cook(4)
print(mySweetPotato.cookedLevel)
print(mySweetPotato.cookedString)

print("接着又烤3分钟")
mySweetPotato.cook(3)
print(mySweetPotato.cookedLevel)
print(mySweetPotato.cookedString)

print("开始加配料 - 辣椒")
mySweetPotato.addCondiments("辣椒")
print(mySweetPotato)

print("又烤了6分钟")
mySweetPotato.cook(6)
print(mySweetPotato)

print("开始加配料 - 番茄酱")
mySweetPotato.addCondiments("番茄酱")
print(mySweetPotato)
