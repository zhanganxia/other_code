import threading
import time


# 唱歌
def sing(num, name, age):
    print("姓名: %s 年龄: %d" % (name, age))
    # 查看当前任务执行线程
    print("sing：", threading.current_thread())
    for i in range(num):
        print("唱歌中...")
        time.sleep(0.01)


# 跳舞
def dance(num):
    # 查看当前任务执行线程
    print("dance：", threading.current_thread())
    for i in range(num):
        print("跳舞...")
        time.sleep(0.01)


if __name__ == '__main__':
    # 查看当前任务执行线程
    print("程序的主线程：", threading.current_thread())

    # 当前程序活动线程的列表
    print("1--------", threading.enumerate())
    # 使用多线程完成多任务
    # 代码执行到此，还是主线程
    # 在主线程创建两个子线程
    # target: 线程执行函数的名字
    # args : 执行函数所需要的参数，这个参数要以元组方式去传
    # kwargs:  执行函数所需要的参数， 这个参数要以字典方式去传
    sing_thread = threading.Thread(target=sing, args=(5,), kwargs= {"name":"汤鹏", "age": 20})
    print(sing_thread)

    dance_thread = threading.Thread(target=dance, args=(3,))
    print(dance_thread)

    # 当前程序活动线程的列表
    print("2--------", threading.enumerate())

    # 开启线程，执行函数中的任务
    sing_thread.start()
    dance_thread.start()

    # 当前程序活动线程的列表
    # 注意: 调用完start方法以后线程才会放入到线程活动列表中
    print("3--------", threading.enumerate())

    # 提示： 线程之间执行顺序是无序的，是操作系统控制。