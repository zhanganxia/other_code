#协程:又称为微线程,可以理解成比线程更小的执行单元,也可以称为用户基线程.协程的执行顺序可以有程序员去控制.
#协程理解:如果在函数里面看见yield的关键字,可以理解成协程
#学习协程的目的:在单线程的基础上完成多任务,多个任务交替执行,可以使用协程
import time

#定义协程1
def work1():
    while True:
        print("work1")
        yield
        time.sleep(0.1)

#定义协程2
def work2():
    while True:
        print("work2")
        yield
        time.sleep(0.1)
#提示:在不开辟线程的基础上,完成多任务可以协程,完成多个任务交替执行
#创建协程
g1 = work1()
g2 = work2()

while True:
    #启动协程
    next(g1)
    next(g2)

