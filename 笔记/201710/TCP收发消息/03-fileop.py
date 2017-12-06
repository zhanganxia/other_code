try:
    file = open("o1.py","rb")

    while True:
        file_data = file.read()

    file.close()

except Exception as e:
    pass
else:
    pass


#with的作用
#1.可以自动捕获异常
#2.在with语句执行完成之后，可以自动释放file资源（即使内部有异常）

    with open("01.py","rb") as file:
        while True:
            file_data = file.read()
   