from collections import Iterable
from collections import Iterator

class StudentList:
    
    def __init__(self):
        self.items = list()
    
    #添加元素
    def append_item(self,item):
        #添加外界传入的元素到指定列表
        self.items.append(item)

    #提供_iter_的方法,该对象就是一个可迭代对象
    #外界调用iter函数会调度下面该方法
    def __iter__(self):
        print("0000000")
        #返回一个迭代器
        #提示:可迭代对象的本质是通过迭代器依次把数据遍历出来的
        student_iterator = StudentIterator(self.items)
        return student_iterator

class StudentIterator:
    #提供构造方法接收外界传入的列表参数
    def __init__(self,items):
        #保存到指定的属性
        self.items = items
        #记录当前的遍历的下标索引
        self.current_index = 0

        result = isinstance(self,Iterator)
        print("StudentIterator是否是迭代器:",result)

    def __iter__(self):
        print("1111")
        return self

    #外界调用next函数会调用下面该方法获取迭代器中下一个值
    def __next__(self):
        print("22222")
        if self.current_index < len(self.items):
            #通过启动迭代器获取对应的数据
            self.current_index += 1
            return self.items[self.current_index - 1]
        else:
            #抛出停止迭代异常
            raise StopIteration

studentList = StudentList()
#添加元素
studentList.append_item("张三")
studentList.append_item("李四")

#iter函数表示:获取可迭代对象的迭代器
# next函数表示:获取迭代器中的下一个值

student_iterator = iter(studentList)
print(student_iterator)  

#通过迭代器获取下一个值
result = next(student_iterator)
print(result)

result = next(student_iterator)
print(result)

#迭代器可以使用for循环值直接遍历取值
#for循环的本质:
    # 首先内部会通过iter函数获取可迭代对象的
    # 迭代器,然后根据next函数依次获取迭代器里面
    # 的数据
for value in student_iterator:
    print(value)


