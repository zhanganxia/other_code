#coding=utf-8
from selenium import webdriver
import time
driver = webdriver.Firefox()
driver.get("http://www.baidu.com/")

# driver.find_element_by_xpath('//a[@class="lb"]').click()

# driver.find_element_by_name("tj_login")
# #点击登录链接
# driver.find_element_by_name("tj_login").click()
# # driver.find_element_by_id('lb').click()

driver.find_element_by_id("u1").find_element_by_name("tj_login").click()
time.sleep(3)
div=driver.find_element_by_xpath("//p[@id='TANGRAM__PSP_8__userNameWrapper']/input")
div.send_keys("605613403@qq.com")

# div=driver.find_element_by_name("tang-content").find_element_by_name("userName")
# div.send_keys("605613403@qq.com")

#输入登录密码
driver.find_element_by_name("password").send_keys("605613403zax")

#点击登录
driver.find_element_by_id("TANGRAM__PSP_10__submit").click()

# #driver.quit()

