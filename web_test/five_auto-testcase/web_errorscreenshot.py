#coding=utf-8
from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.get("http://www.baidu.com")

#捕捉百度输入框异常
try:
    browser.find_elemnet_by_id("kwsss").send_keys("selenium")
    browser.find_elemnet_by_id("su").click()
    time.sleep(2)
except:
    browser.get_screenshot_as_file("/home/web_test/error.png")

#browser.quit()
