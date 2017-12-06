#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest,time,os

source = open("用户名文件路径")#用户名文件
un = source.read()#读取用户名
source.close()

source2 = open("密码文件路径")#密码文件
pw = source2.read()#读取密码
source2.close()

def login(self):
    driver = self.driver
    driver.maximize_window()
    driver.find_element_by_id("user_name").clear()
    driver.find_element_by_id("user_name").send_keys(un)
    driver.find_element_by_id("user_pwd").clear()
    driver.find_element_by_id("user_pwd").send_keys(pw)
    driver.find_element_by_id("dl_an_submit").click()
    time.sleep(3)  

#运行之前的webcloud.py文件，程序可以正常的执行。虽然这样做比较丑，但确实达到了数据数据与脚本分离的目的
# 
# 缺点：
# 虽然目的达到了这，但这样的实现有很多问题：
# 1.用户名密码分别在不同的文件里，修改用户名和密码比较麻烦。
# 2.username.txt和password.txt文件中只能保存一个用户密码，无能很好的循环读取
# 
# 