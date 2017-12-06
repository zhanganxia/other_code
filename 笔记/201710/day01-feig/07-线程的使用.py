#encoding=utf-8
import threading

def sing(num):
    #查看当前任务执行线程
    print("sing:",threading.current_thread())
    for i in range(num):
        print("唱歌中...")

def dance(num):
    #查看当前任务执行线程
    print("dance:",threading.current_thread())
    for i in range(num):
        print("***跳舞中")

if __name__ == '__main__':
    #查看当前任务执行线程
    print("程序的主线程：",threading.current_thread())

    #当前程序活动线程的列表
    print("-"*20)
    print(threading.enumerate(),)
    
    sing_thread = threading.Thread(target = sing,args=(5,))
    print(sing_thread)
    dance_thread = threading.Thread(target = dance,args=(5,))
    print(dance_thread)

    sing_thread.start()
    dance_thread.start()

    #threading active_count-->查看当前活动线程数量
    # sing()
    # dance()
