#encoding=utf-8
#打印一条横线
#1.直接对原函数进行修改
def printLine(n):
    i=0
    while i<n:
        print("_"*30)
        i+=1
#1.修改原函数
#这种方法不太好，应为这个printLine函数可能在其他的的地方已经被调用很多次
#而此时进行修改，那么也就意味着原来调用这个函数的地方，也发生了变化

#2.自己定义一个新的函数

def printLine2():
    print("_"*30)

def printNumsLine(n):
    i=0
    while i<n:
        printLine2()
        i+=1

num = int(input("请输入要打印的个数："))
printNumsLine(num)