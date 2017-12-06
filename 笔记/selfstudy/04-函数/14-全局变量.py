#在函数的外边定义的变量就叫做全局变量
num=100

def test1():
    #如果在函数中直接修改全局变量，那么会产生异常
    #如果真的需要进行修改，那么可以子啊函数里面声明
    global num
    print(num)
    num+=2
    print(num)

def test2():
    print(num)
test1()
test2()

#全局变量的优点：保证数据的安全性，在其他函数中都可以用