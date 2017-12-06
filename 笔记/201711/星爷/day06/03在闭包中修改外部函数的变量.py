#encoding=utf-8

#python2 在闭包中修改外部函数的变量
def yanzhen(func):
    hh_list = [func]
    def inner():
        #nonlocal func
        hh_list[0] += 2
        if hh_list[0] >= 100:
            print("tesing",hh_list[0])
    return inner

hh = yanzhen(100)
hh()

#python3在闭包中修改外部函数的变量
def yanzhen(func):
    def inner():
        nonlocal func
        func += 2
        if func >= 100:
            print("tesing",func)
    return inner

hh = yanzhen(100)
hh()

# @yanzhen
# def login(num):
#     print("正在验证您的身份，请稍后",num)

# login(100)



        