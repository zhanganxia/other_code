# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Firefox()
url = "http://www.baidu.com"
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(5)

#进入搜索设置项
link = driver.find_element_by_link_text("设置")
ActionChains(driver).move_to_element(link).perform()

driver.find_element_by_link_text("搜索设置").click()
time.sleep(2)

# #设置每页搜索结果为50条
choice = driver.find_element_by_name("NR")
choice.find_element_by_xpath("//option[@value='50']").click()
time.sleep(2)

#保存设置
driver.find_element_by_xpath("//a[@class='prefpanelgo']").click()
time.sleep(3)

#弹框处理
#accept - 点击【确认】按钮
#dismiss - 点击【取消】按钮
driver.switch_to_alert().accept()

#跳转到百度首页后，进行搜索表
driver.find_element_by_id('kw').send_keys("selenium")
driver.find_element_by_id('su').click()
time.sleep(3)

driver.quit()