#coding=utf-8
#coding=utf-8
from selenium import webdriver
import login,quit
import time
#登录模块
def login(driver):
    driver.find_element_by_id("u1").find_element_by_name("tj_login").click()
    time.sleep(3)
    div=driver.find_element_by_xpath("//p[@id='TANGRAM__PSP_8__userNameWrapper']/input")
    div.send_keys("605613403@qq.com")
    driver.find_element_by_name("password").send_keys("605613403zax")
    driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
