#定义一个函数，完成3个数的求和
def add3Num(a,b,c):
    result = a+b+c
    return result
#定义一个函数，完成求3个数的平均值
def averge3Num(a,b,c):
    result = a+b+c
    averge = result/3
    return averge

def averge3Num_2(A,B,C):
    result = add3Num(A,B,C)
    averge = result/3
    return averge


result = averge3Num_2(44,55,66)
print(result)

# result = add3Num(11,22,33)
# print(result)