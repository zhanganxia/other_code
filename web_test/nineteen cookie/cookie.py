#coding=utf-8
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("http://www.youdao.com")

#获得cookies信息
cookie=driver.get_cookies()
#将获得cookies的信息打印
print cookie
driver.quit()