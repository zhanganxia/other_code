#coding=utf-8
from selenium import webdriver
browser = webdriver.Firefox()
browser.get("http://m.mail.10086.cn")
#参数数字为像素点
print "设置浏览器宽480、高800显示"
browser.set_window_size(480,800)









#browser.quit()

