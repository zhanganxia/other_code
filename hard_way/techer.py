#encoding=utf-8
import random

#1.先定义一个列表，用来存储8位老师的名字
teachers = ['xiaowang','xiaoli','xiaozhang','xiaosong','xiaozhao','xiaoliu','xiaowu']

#2.定义一个列表，这里有只有3个空的办公室，用来等待其他老师进行加入
offices = [[],[],[]]

#3.通过循环的方式把8位老师随机分配到，3个办公室中
#注意：所谓的随机奉陪，即获取一个随机的办公室号，然后把这个老师添加到里面即可

for name in teachers:
    index = random.randint(0,2)
    offices[index].append(name)

#4.输出每个办公室里面老师的信息
#print(offices)
i = 1
for room in offices:
    #print(room)
    print("办公室%d"%i)
    for teacherName in room:
        print(teacherName)
    print("-"*20)
    i+=1

#扩展：怎样保证每个办公室里边老师的人数至少是2个人