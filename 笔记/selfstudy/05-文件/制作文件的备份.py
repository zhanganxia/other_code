#encoding=utf-8
#输入文件的名字，然后程序自动完成对文件的备份

#1.输入要备份的文件名
oldFileName = input("请输入要备份的文件名：")
#2.读文件(以只读的方式打开文件)
oldFile = open(oldFileName,'rb')
#3.获取文件的后缀
fileFlagNum = oldFileName.rfind('.')
if fileFlagNum > 0:
    fileFlag = oldFileName[fileFlagNum:]
#4.定义复制文件名
newFileName = oldFileName[:fileFlagNum]+'[附件]'+fileFlag
print(newFileName)

#创建新文件
newFile = open(newFileName,'wb')
#5.将读到的数据依次写入新的文件中
for lineContent in oldFile.readlines():
    newFile.write(lineContent)
#6.关闭文件
oldFile.close()
newFile.close()

