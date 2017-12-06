#coding=utf-8
import os

funFlag = 1#1:表示添加标志  2:表示删除标志

folderName = '/home/kk/other_code/笔记/A/B'

#获取指定路径的所有文件名字
dirList = os.listdir(folderName)

#遍历输出所有文件名字
for name in dirList:
    print(name) 

    if funFlag == 1:
        
        newName = 'zax-'+name
    else funFlag == 2:
        num = len('zax-')
        newName = name[num:]
    print newName

    os.rename(folderName+name,folderName+newName)