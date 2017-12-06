#import Iterable

#迭代器完成斐波那契数列
#定义迭代器
class Fib:
    def __init__(self,num):
        #记录生成斐波那契数列的个数
        self.num = num
        #初始化a,b的值
        self.a = 0
        self.b = 1
        #记录当前迭代的索引
        self.index = 0
    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.num:
            result = self.a
            self.a,self.b = self.b,self.a+self.b
            #计算每次生成索引
            self.index += 1
            return result
        else:
            raise StopIteration

#创建迭代器
fib = Fib(10)

# result = next(fib)
# print(result)

# result = next(fib)
# print(result)

for i in fib:
    print(i)





