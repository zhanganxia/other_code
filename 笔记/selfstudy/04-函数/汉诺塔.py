#汉诺塔:对柱子编号为a,b,c,将所有圆盘从a移动到c
def move(n,a,b,c):
    if n == 1:
        print(a, '-->',c)
        return
    else:
        move(n-1,a,c,b)#将前n-1个盘子从a移动到b上
        print(a,'-->',c)#将a上的最后一个盘子移动到c
        move(n-1,b,a,c)#将b上的n-1个盘子移动到c上
n = int(input("请输入汉诺塔的层数:"))

move(n,'X','Y','Z')