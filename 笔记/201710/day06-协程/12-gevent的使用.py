#gevent是封装的是greenlet,根据耗时操作自动进行协程间切换执行
import gevent
import time
from gevent import monkey

#打补丁,让gevent能够识别系统的耗时操作,提示:这句代码一定要先只想
monkey.patch_all()

#任务1
def work1():
    for i in range(5):
        print("work1....")
        #不打补丁gevent不认为是耗时
        time.sleep(0.1)
        #gevent.sleep(0.1)

#任务2
def work2():
    for i in range(6):
        print("work2....")
        #不打补丁gevent不认为是耗时
        time.sleep(0.1)
        #gevent.sleep(0.1)

#创建协程指派任务
#第一个参数是函数名
g1 = gevent.spawn(work1)
g2 = gevent.spawn(work2)

g1.join()
g2.join()
