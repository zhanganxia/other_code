# coding=utf-8  
import time  
from selenium import webdriver  
  
  
driver = webdriver.Firefox()  
driver.maximize_window()  
driver.implicitly_wait(6)  
driver.get("https://www.baidu.com")  
time.sleep(1)  
  
driver.get_screenshot_as_file("\\Home\\web_test\\baidu.png")  
driver.quit()  