#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest,time

class Login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://passport.kuaibo.com"
        self.verificationErrors = []
        self.accept_next_alert = True
#私有云登录用例
def test_login(self):
    driver = self.driver
    driver.get(self.base_url "/login/?referrer=http%3A%2F%2Fwebcloud.kuaibo.com%2F")

    driver.maximize_window()
    #登录
    driver.find_element_by_id("user_name").clear()
    driver.find_element_by_id("user_name").send_keys("username")
    driver.find_element_by_id("user_pwd").clear()
    driver.find_element_by_id("user_pwd").send_keys("123456")
    driver.find_element_by_id("dl_an_submit").click()
    time.sleep(3)

    #新功能引导
    driver.find_element_by_class_name("guide-ok-btn").click()
    time.sleep(3)

    #退出
    driver.find_element_by_class_name("Usertool").click()
    time.sleep(2)
    driver.find_element_by_link_text("退出").click()
    time.sleep(2)

def tearDown(self):
    self.driver.quit()
    self.assertEqual([],self.verificationErrors)
if _name_ == "_main_":
      unittest.main()
    