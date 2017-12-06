import multiprocessing
import time

def copy_work():
    print("正在复制中....",multiprocessing.current_process().pid)
    time.sleep(1)


if __name__ == '__main__':
    
    pool = multiprocessing.pool(3)

    for i in range(3):
        pool.apply(copy_work)
    
    pool.close()
