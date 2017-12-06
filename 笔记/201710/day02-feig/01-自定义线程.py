import threading
import time

#自定义线程
class MyThread(threading.Thread):

    def __init__(self,num):
        #需要调用父类的构造方法
        super(MyThread,self).__init__()
        #使用属性记录外界传入参数
        self.num = num

    def show_msg(self):
        for i in range(5):
            print("线程在创建...")
            time.sleep(0.1)

    def run(self)：
    #提示：以后线程执行的所有的任务可以在run方法里面调用
    self.show_msg()