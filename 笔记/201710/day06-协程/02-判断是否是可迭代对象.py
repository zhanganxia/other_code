#列表、字符串、元组、字典、集合、range
from collections import Iterable

#判断列表是不是可迭代对象
result = isinstance(["hahah","读嘟嘟"],Iterable)
print("列表是否是可迭代对象:",result)

#判断字典是否是可迭代的对象
result = isinstance({"name":"zax","age":22},Iterable)
print("判断字典是否是可迭代的对象:",result)

#判断元组是否是可迭代对象
result = isinstance(("name","zax","age"),Iterable)
print("判断元组是否是可迭代对象:",result)

#判断字符串是否是可迭代对象
result = isinstance("hahahahah",Iterable)
print("字符串是否是可迭代对象:",result)

#判断集合是否是可迭代的对象
result = isinstance({1,1,2,3},Iterable)
print("集合是否是可迭代对象:",result)

#判断rangge是否是可迭代对象
result = isinstance(range(3),Iterable)
print("range是否是可迭代对象:",result)

#整形和自定义类是不可迭代对象
print("-"*20)
#判断整型是否是可迭代对象
result = isinstance(2,Iterable)
print("整型是否是可迭代对象:",result)

#判断自定义类是否是可迭代对象
class StudentList:
    pass
stulist = StudentList()
result = isinstance(stulist,Iterable)
print("自定义类是否是可迭代对象:",result)





