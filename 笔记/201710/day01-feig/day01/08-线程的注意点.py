# 注意点
# 1. 线程之间执行顺序是无序
# 2. 主线程会等待所有的子线程任务执行完成以后程序再退出
import time
import threading


# 任务1
def work1():
    print("子线程:", threading.current_thread())
    while True:
        print("工作中.....")
        time.sleep(0.3)


if __name__ == '__main__':
    # 主线程创建子线程
    work_thread = threading.Thread(target=work1)
    # 设置成为守护主线程， 主线程退出了，那么子线程直接销毁不执行代码了, 以后线程的销毁要依赖主线程
    work_thread.setDaemon(True)
    # 开启线程执行任务
    work_thread.start()

    print("主线程:", threading.current_thread())
    # 主线程等待2秒程序就退出
    time.sleep(2)
    print("主线程的任务执行完成了。")
    exit()



