import multiprocessing

if __name__ == '__main__':
    #创建消息队列
    queue = multiprocessing.Queue(5)

    queue.put("hello")
    queue.put([3,4,5])
    queue.put({"name":"张三","age":20})
    queue.put(("Apple","watermelon"))
    queue.put({"哈哈","呼呼"})

    #获取数据
    print(queue.get())
    print(queue.get())
    print(queue.get())
    print(queue.get())
    print(queue.get())
