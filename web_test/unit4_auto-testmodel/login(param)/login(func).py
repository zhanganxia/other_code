#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest,time,os
import userinfo #导入函数

# 通过两个变量，来接收调用函数获得用户名&密码
us,pw = userinfo.fun()

#打印两个变量
print us,pw

def login(self):
    driver = self.driver
    driver.maximize_window()
    driver.find_element_by_id("user_name").clear()
    driver.find_element_by_id("user_name").send_keys(un)
    driver.find_element_by_id("user_pwd").clear()
    driver.find_element_by_id("user_pwd").send_keys(pw)
    driver.find_element_by_id("dl_an_submit").click()
    time.sleep(3)  