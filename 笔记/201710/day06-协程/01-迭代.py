#使用for循环迭代的对象：列表、字符串、元组、字典、集合、range

for i,value in enumerate(["苹果","香蕉"]):
    print(i,value)

print("-"*20)

for mychar in "hello":
    print(mychar)

print("-"*20)

for value in (1,2,3,4):
    print(value)
print("-"*20)

for key,value in {"name":"zax","age":18}.items():
    print(key,value)
print("-"*20)

for value in {"hah","dudu"}:
    print(value)
print("-"*20)

for i in range(3):
    print(i)
#总结：使用for循环遍历取值的过程叫做迭代
#能够使用for循环遍历取值的对象叫做可迭代对象，比如：列表。。。

#整型是不可迭代对象
#自定义的类不是可迭代的对象
class StudentList:
    pass
studentlist = StudentList()
for value in studentlist:
    print(value)




