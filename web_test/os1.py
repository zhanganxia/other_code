# -*- coding: utf-8 -*-
#通过CSS方式来勾选一组元素，打印当前所勾选元素的个数并对最后一个勾选的元素取消勾选
from selenium import webdriver
import os

driver = webdriver.Firefox()
file_path = 'file://' + os.path.abspath('checkbox.html')
driver.get(file_path)

#选择所有的type为checkbox的元素并单击勾选
checkboxes = driver.find_elements_by_css_selector('input[type=checkbox]')
for checkbox in checkboxes:
    checkbox.click()

#打印当前页面上type为checkbox的个数
print len(driver.find_elements_by_css_selector('input[type=checkbox]'))

#把页面上最后1个checkbox的勾去掉
driver.find_elements_by_css_selector('input[type=checkbox]').pop().click()

driver.quit()
