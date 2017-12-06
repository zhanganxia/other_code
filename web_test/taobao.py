# -*- coding: utf-8 -*-
from time import sleep
import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()  # 创建火狐浏览器对象
        #cls.driver.get("https://www.taobao.com/")  # 导航到淘宝主页
        #cls.driver.maximize_window()
        #time.sleep(random.randint(1,2))


    def test_search_by_category(self):
        self.driver = webdriver.Firefox()  # 创建火狐浏览器对象
        self.driver.get("https://www.taobao.com/")  # 导航到淘宝主页
        self.driver.maximize_window()
 	search_field = self.driver.find_element_by_id("q")  # 获取到搜索框
        print search_field
        search_field.clear()
        search_field.send_keys("iPhone 6s Plus" + Keys.RETURN)
        #search_field.send_keys("iPhone 6s Plus")
        # 断言：检查本页显示出来的产品个数是否为48个
        # 定位到“搜索结果汇总”元素，注意find_element(s)的不同
	time.sleep(random.randint(2,3))
        result = self.driver.find_elements_by_css_selector("div[class='total']")
        print "#########\n"
        print result
        print result.text
        # 断言：检查页数是否为35页
        # self.assertEqual('共30页，'，result.text)
        # 获取字符串的第3到倒数第三个字符位，以获取页数
        pageNum = int(result.text[2:-3])
        print(pageNum)
        self.assertEqual(13,pageNum)
        print (result.text)

        #下面开始计算产品总数
        sum = 0
        for i in range(pageNum):
            sleep(3)
            products = self.driver.find_elements_by_css_selector("div[class='item g-clearfix']")
            sum = sum + len(products)
            print(len(products)) #计算本页产品数
            j=1
            for pt in products:
                #将滚动条滚动到pt产品所在的位置
                self.driver.execute_script("arguments[0].scrollIntoView();", pt)
                strTxt = pt.get_attribute("textContent").upper() #得到的商品的文字并转换为大写
                try:
                    self.assertIn("APPLE",strTxt)
                    self.assertIn("IPHONE",strTxt)
                    self.assertIn("6S",strTxt)
                    self.assertIn("PLUS",strTxt)
                    print("第%d页第%d个产品"%(i+1,j))
                except Exception as e:
                    print("第%d页第%d个产品验证失败"%(i+1,j))
                j +=1
            #开始点下一页
            if i< pageNum - 1:
                self.driver.find_element_by_link_text("下一页").click()
        print(sum)
        cSum = self.driver.find_element_by_class_name("result-info").text[0:3]
        self.assertEqual(sum,int(cSum))
        # 得到元素节点下的所有文字（可见与不可见）
        # products[0].get_attribute('textContent')
    
    @classmethod
    def tearDownClass(cls):
        #关闭浏览器对象
        cls.driver.quit()

if __name__ =='__main__':
    unittest.main()

