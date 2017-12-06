#encoding=utf-8

#定义函数
# def add(x,y):
#     return x+y

# def subtract(x,y):
#     return x-y

# def muitiply(x,y):
#     return x*y

# def divide(x,y):
#     return x/y

def math_num(x,y,op):
    if op == "+":
        return x+y
    elif op == "-":
        return x-y
    elif op == "*":
        return x*y
    elif op == "/":
        return x/y
    else:
        return "请输入正确的运算符!"

def main():
    #x,y,op=input("请输入两个数字和运算符：")
    print(math_num(22,33,"-"))

if __name__=="__main__": 
    main()