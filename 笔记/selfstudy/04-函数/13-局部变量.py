import time
def test1():
    num = 100
    print(num)

def test2():
    num = 200
    print(num)

    time.sleep(1)
    num = num+100
    print(num)

#在函数里面定义的变量，就叫做局部变量
#它只在定义它的函数种有效，出了这个函数，它就没有了

test1()
test2()