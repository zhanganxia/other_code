#coding=utf-8
from selenium import webdriver
import os,time

driver = webdriver.Firefox()

#打开文件上传文件页面
file_path = 'file://'+os.path.abspath('upload_file.html')
driver.get(file_path)

#定位上传按钮，添加本地文件
driver.find_element_by_name("file").send_keys('/home/kk/h2.py')
#time.sleep(2)

#driver.quit()