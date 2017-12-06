import multiprocessing
import time
import os

#显示学生信息
def show_student_info(sid,name,age):
    for i in range(10):
        print("序号：%d,姓名: %s,年龄：%d"%(sid,name,age))
        time.sleep(0.1)

if __name__ == '__main__':
    stu_process = multiprocessing.Process(target=show_student_info,args=(2,),
                                            kwargs={"name":"zax","age":22})
    #stu_process = multiprocessing.Process(target=show_student_info,args(2,),kwargs={"name":"zax","age" = 22})
    
    stu_process.start()
    exit()
    
