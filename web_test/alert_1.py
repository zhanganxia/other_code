#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Firefox()
driver.get("http://www.baidu.com/")
driver.implicitly_wait(5)
#time.sleep(2)
#点击打开搜索设置
# menu = driver.find_element_by_link_text(u"设置")
# # driver.find_element_by_name("tj_setting").click()
# # menu = driver.find_element_by_class_name("pf")
# # menu = driver.find_element_by_id("tj_settingicon").find_element_by_link_text(u'搜索设置')
menu = driver.find_elements_by_name("tj_settingicon").pop().click()
ActionChains(driver).move_to_element(menu).perform()

# driver.find_element_by_link_text(u"搜索设置").click()
# driver.find_element_by_xpath('//*[@id="u1"]/a[8]').click()
driver.find_element_by_link_text(u"搜索设置").click()
time.sleep(1)
driver.find_element_by_id("sh_1").click()
#点击保存设置
driver.find_element_by_xpath("//div[@id='gxsxButton']/input").click()

#获取网页上的警告信息
alert=driver.switch_to_alert()

#接收警告信息
alert.accept()

#driver.quit()


