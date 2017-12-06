#encoding=utf-8
import time

def yanzhen(func):
    def inner(*args,**kwargs):
        print("信息验证中...")
        msg = func(*args,**kwargs)
        print("*********验证结束*********")
        #return msg
    return inner

def getruntime(func):
    def get_inner(*args,**kwargs):
        start_time = time.time()
        print("开始时间：%f"%start_time)
        func(*args,**kwargs)
        end_time = time.time()
        print("结束时间：%f"%end_time)
        delta_time = end_time - start_time
        print("运行此函数耗时%f"%delta_time)
    return get_inner



@yanzhen
@getruntime
def login(username):
    #return "%s您的信息正在验证请稍后..." %username
    print("%s，您的信息正在验证请稍后..."%username)
    for i in range(5):
        time.sleep(0.3)

login("zax")