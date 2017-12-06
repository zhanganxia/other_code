import time


# 任务1
def dance():
    for i in range(5):
        print("跳舞中....")
        time.sleep(0.1)


# 任务2
def sing():
    for i in range(5):
        print("唱歌中...")
        time.sleep(0.1)


# 提示： 默认情况程序启动只有一个线程， 就是主线程
if __name__ == '__main__':
    dance()
    sing()