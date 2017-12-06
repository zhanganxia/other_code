from greenlet import greenlet
import time
#greenlet 对协程进行封装(yield)封装,手动切换到不同协程执行任务

#定义任务1
def work1():
    for i in range(10):
        print("work1...")
        #切换到协程2里面执行
        g2.switch()
        time.sleep(0.1)

#定义任务2
def work2():
    for i in range(10):
        print("work2.....")
        #切换到协程1里面执行
        g1.switch()
        time.sleep(0.1)

#创建协程
g1 = greenlet(work1)
g2 = greenlet(work2)

#启动协程执行任务1
g1.switch()




