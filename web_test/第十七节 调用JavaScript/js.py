#coding=utf-8
from selenium import webdriver
import time,os

driver = webdriver.Firefox()
file_path = 'file://' + os.path.abspath('js.html')

driver.get(file_path)

####通过JS隐藏中的元素####第一种方法
#隐藏文字信息
driver.execute_script('$("#tooltip").fadeOut();')
print '11111'
time.sleep(5)

#隐藏的按钮
button = driver.find_element_by_class_name('btn')
driver.execute_script('$(arguments[0]).fadeOut()',button)
time.sleep(5)

#driver.quit()