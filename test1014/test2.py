#encoding=utf-8
import string

i=1
while i<=9:
    j=1
    while j<=i:
        print("%d*%d=%-2d "%(j,i,j*i),end='')
        j+=1
    print("\n")
    i+=1