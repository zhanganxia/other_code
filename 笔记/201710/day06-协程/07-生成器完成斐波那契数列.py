#定义生成器
#在函数中如果出现yiled关键字表示是生成器
def feib2(num):
    #初始化前面两个值
    a = 0
    b = 1

    #记录生成数据的索引
    index = 0
    print("1"*10)
    while index < num:
        result = a
        a,b = b,a+b
        index += 1
        print("2"*15)
        yield result
        print("3"*20)

feib = feib2(5)

result = next(feib)
print(result)

result = next(feib)
print(result)

result = next(feib)
print(result)
result = next(feib)
print(result)



