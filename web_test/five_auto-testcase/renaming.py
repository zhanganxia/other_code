#勾选重命名的文件
driver.find element by xpath("/html/body/div/div[2]/div[2]...").click()
time.sleep(3)

#鼠标移动到”更多“按钮弹下拉框
element=driver.find_element_by_class_name("more-fe")
ActionChains(driver).move_to_element(element).perform()
time.sleep(2)
#在li标签（更多 下拉框）中筛选到data-action==rename(重命名)选项点击
lis=driver.find_element_by_tag_name('li')
for li in lis:
    if li.get_attribute('data-action')=='rename':
        li.click()
    time.sleep(2)
#在input标签中筛选type==text的重命名输入框
inputs=driver.find_element_by_tag_name('input')
for input in inputs:
    if input.get_attribute('type') == 'text':
        input.send_keys(u"新文件名") #进行重命名操作
        input.send_keys(Keys.ENTER) #回车确认重命名
        time.sleep(2)