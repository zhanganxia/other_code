#coding=utf-8
from selenium import webdriver
import login,quit
import time
driver = webdriver.Firefox()
driver.get("http://www.baidu.com/")

login.login(driver)
quit.quit_(driver)