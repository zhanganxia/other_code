#定义生成器
#在函数里面如果出现yield关键字表示是生成器

def fibnq(num):
    #初始化斐波那契前两个数值
    a = 0
    b = 1

    #定义当前数值的索引
    index = 0
    print("----111-----")
    while index < num:
        result = a
        a,b = b,a+b
        index += 1
        print("---2---")

        yield result
        print("---3----")
        return "hhh"


feib = fibnq(5)
# for i in range(5):
#     result = next(feib)
#     print(result)
while True:
    #获取return返回的值
    try:
        result = next(feib)
        print(result)
    except StopIteration as e:
        #获取return返回值
        print(e.value)
        break
#总结:
# 1.在生成器里面可以有return关键字,语法上没有什么问题,
#但是执行return代码以后,会抛出停止迭代异常
#2.return 关键字只能返回一次结果
#3.yield 可以返回多次结果,每次启动生成器都可以使用yield返回结果
