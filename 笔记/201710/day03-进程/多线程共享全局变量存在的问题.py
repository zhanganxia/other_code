#encoding=utf-8
import threading
import time

num = 0

def write_num():
    global num
    for i in range(1000000):
        num+=1
        #num.append(i)
    print(num)
def read_num():
    # global num
    # print("读到num的值是：%s"%num)
    global num
    for i in range(1000000):
        num+=1
    print("线程2的运行结果:%d"%num)

if __name__ == '__main__':
    write_thread = threading.Thread(target=write_num)
    read_thread = threading.Thread(target=read_num)

    write_thread.start()
    write_thread.join()
    #time.sleep(1)
    read_thread.start()
    

