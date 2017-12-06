import multiprocessing
import time

#写入数据任务
def write_data(queue):
    for i in range(10):
        queue.put(i)
        time.sleep(0.1)
#读取数据任务
def read_data(queue):
    while True:
        if queue.empty():
            break
        print(queue.get())

if __name__ == '__main__':
    #创建进程池
    pool = multiprocessing.Pool(2)

    #创建进程池中的消息队列
    queue = multiprocessing.Manager().Queue()
    #使用进程池中的空闲进程执行对应写入数据的任务
    #扩展：返回一个对象
    result = pool.apply_async(func=write_data,args=queue)

    result.wait(1)
    print(result)

    pool.close()
    pool.join()
