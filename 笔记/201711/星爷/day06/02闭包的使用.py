def line1(k,b):
    def set_x(x):
        return k*x + b
    return set_x
#Y指向 set_x 通过调用y来设置x的值
y = line1(1,2)
y1 = y(2)
print(y1)
#函数一旦引用了闭包之后和类非常类似