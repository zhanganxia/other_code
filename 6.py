#encoding=utf-8
a=[]
for i in range(1,6):
    #print(i)
    b=input("请输入第%d个数:"%i)
    num=float(b)
    a.append(num)
print sum(a)

#切片(左闭右开)：取一个list获tupe的部分元素
#tuple也是一种list，只是tuple不可变
