#coding=utf-8

f = open('1.txt','r')

content = f.readlines()

print(type(content))

i=1
for temp in content:
    print("%d:%s"%(i,temp))
    i+=1
f.close()
