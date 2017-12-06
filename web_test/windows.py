#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

driver = webdriver.Firefox()
# js='window.open("https://www.baidu.com");'
# driver.execute_script(js)
driver.get("http://www.baidu.com/")
driver.maximize_window() # 窗口最大化

driver.find_element_by_id("u1").find_element_by_name("tj_login").click()
baidu=driver.current_window_handle

#打来注册新窗口
driver.execute_script("$(window.open('https://www.baidu.com'))")
time.sleep(3)


#获得所有窗口
allhandles=driver.window_handles
print allhandles

#循环判断窗口是否为当前窗口
for handle in allhandles:
    print '1111111'
    print handle
    if handle == baidu:
        print handle
        print '222222'
        driver.switch_to_window(baidu)
        print 'now register window!'
        #切换到邮箱注册标签
        #driver.find_element_by_id("mailRegTab").click()
        div=driver.find_element_by_xpath("//p[@id='TANGRAM__PSP_8__userNameWrapper']/input")
        div.send_keys("605613403@qq.com")
        driver.find_element_by_name("password").send_keys("605613403zax")
        time.sleep(5)
        driver.close()
    else :
        new_baidu = handle
print baidu +' 1111'
#回到原先的窗口
#else handle !== nowhandle:
driver.switch_to_window(new_baidu)
print baidu +' 2222'
driver.find_element_by_id("kw").send_keys(u"注册成功！")
time.sleep(3)
#driver.quit()
        
    

