# -*- coding: utf-8 -*
from sys import argv

script,filename = argv

txt = open(filename)

print "Here’s your file %r:" % filename
print txt.read()
txt.close()
print "Type the filename again:"
file_again = raw_input(">")

txt_again = open(file_again)

print txt_again.read()
txt_again.close()

#close-关闭文件
#read-读取文件内容。可以把结果赋值给一个变量
#readline - 读取文本文件中的一行。
#truncate-清空文件，请小心使用该命令。
#write(stuff)-将stuff写入文件

