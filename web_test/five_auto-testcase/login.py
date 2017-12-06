#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import Action_Chains
import time

driver = webdriver.Firefox()
driver.get("http://passport.kuaibo.com/login/?referrer-http")

driver.maximize_windows()#浏览器最大化

#登录
driver.find_element_by_id("user_name").send_keys("testing360")
driver.find_element_by_id("user_pwd").seend_keys("132445")
driver.find_element_by_id("dl_an_submit").click()
time.sleep(3)

#获取用户名
now user=driver.find_element_by_xpath("//div[@id='Nav']/ul/li[4]/a[1]/span").text
#用户名是否等于虫师，不等于将抛出异常

if now_user==u'虫师'
    print '登录成功'
else:
    raise NameError('user name error!')
#退出
driver.find_element_by_class_name("Usertool").click()
time.sleep(2)
driver.find_element_by_link_text("退出").click()
time.sleep(2)
driver.close()