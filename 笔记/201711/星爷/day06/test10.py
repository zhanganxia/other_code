import time
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

@getruntime
def login(username):
    print("您的信息正在验证请稍后...%s"%username)
    for i in range(5):
        time.sleep(0.3)
login("zax")
