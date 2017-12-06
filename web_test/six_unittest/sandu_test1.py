# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Web(unittest.TestCase):#web类继承unittest.TestCase类，从TestCase类继承是告诉unittest模块的方式，这是一个测试案例
    #setUp用于设置初始化的部分，在测试用例执行前，这个方法中的函数将先被调用。这里将浏览器的调用和URL的访问放到初始化部分
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://app3.sanduspace.cn/sandu/pages/jsp/index.jsp"
        self.verificationErrors = []#脚本运行时，错误的信息将被打印到这个列表中
        self.accept_next_alert = True#是否继续接受下一个警告
    

    #test_web中放置的就是我们的测试脚本了，我们执行的脚本就在这里
    def test_web(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("account").clear()
        driver.find_element_by_id("account").send_keys("18218366324")
        driver.find_element_by_id("login").click()
        driver.find_element_by_link_text(u"系统管理").click()
        driver.find_element_by_id("left_menu_3").click()
        driver.find_element_by_link_text(u"用户列表").click()
        driver.find_element_by_link_text(u"角色管理").click()
        driver.find_element_by_id("left_menu_84").click()
        driver.find_element_by_link_text(u"版本管理").click()
        driver.find_element_by_link_text(u"产品管理").click()
    
    #is_element_present函数用来查找页面元素是否存在
    #try...except...为python语言的异常捕捉
    #is_element_present函数在这里用处不大，通常删除，因为判断页面元素是否存在一般都加在testcase中
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    #对弹框异常的处理
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    #关闭警告以及对得到文本框的处理
    #try...finally...为python的异常处理
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
   
   # tearDown方法在每个测试方法执行后调用，这个地方做所有测试用例执行完成的清理工作，如退出浏览器等
    def tearDown(self):
        self.driver.quit()
        #对前面的verificationErrors方法获得的列表进行比较；如查verificationErrors列表中的信息不为空，输出列表中的报错信息
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()#main函数用来测试类中以test开头的测试用例
