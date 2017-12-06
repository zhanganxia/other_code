#打开一个已经存在的文件
f = open("1.txt","r")

#查找当前位置
position = f.tell()
print("当前文件位置：",position) 

#重新设置位置
f.seek(-1,2)

#读取到的数据为：文件最后3个字节数据
str = f.read()
print("读取的数据是：",str)

f.close()

