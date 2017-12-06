from collections import Iterable
from collections import Iterator

class StudentList:
    def __init__(self):
        self.items = list()
    
    #添加元素
    def append_item(self,item):
        #添加外界传入的元素到指定列表
        self.items.append(item)

    #提供__iter__的方法,该对象就是一个可迭代对象
    def __iter__(self):
        #返回一个迭代器
        #提示:可迭代对象的本质是通过迭代器依次把数据遍历出来
        student_iterator = StudentIterator(self.items)

#在类里面定义__iter__和__next__的这两个方法表示就是迭代器,
# 迭代器就是记录当前遍历位置及获取下一个位置的值,
# 自定义迭代器

class StudentIterator:
    #提供构造方法接收外界传入的参数列表
    def __init__(self,items):
        #保存到指定的属性
        self.items = items
        #记录当前的遍历的下标索引
        self.current_index = 0
        
        result = isinstance(self,Iterator)
        print("StudentIterator是否是迭代器:", result)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.items):
            #通过启动迭代器获取对应的数据
            self.current_index += 1
            return self.items[self.current_index - 1]
        else:
            #抛出停止迭代异常
            raise StopIteration

studentList = StudentList()
#添加元素
studentList.append_item("zax")
studentList.append_item("ljq")

#判断该对象是否是可迭代对象
result = isinstance(studentList,Iterable)
print("StudentList是否是可迭代对象:",result)

for value in studentList:
    print(value)





    