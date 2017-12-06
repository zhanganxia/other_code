#判断当前文件个数
inputs=driver.find_elements_by_tag_name('input')
n=0
for i in inputs:
    if i.get_attribute('type')=="checkbox":
        n=n+1
print u"当前列表文件为%d" %n
#删除操作
driver.find_element by xpath("/html/body/div/div[2]/div[2]....").click()
driver.find_element_by_class_name("dele").click()
driver.find_element_by_xpath("/html/body/div/div[]...").click
time.sleep(4)

#再次获取当前文件的个数
inputs=driver.find_element_by_tag_name('input')
ns=0
for ii in inputs:
    if ii.get_attribute('type')=="checkbox":
        ns=ns+1
print u"当前列表文件为%d" %ns

#判断执行删除单个文件之后比删除文件之后文件减1，否则抛异常
f ns==n-1:
print"ok!"
else:
    raise NameError('删除文件失败！！')
#收藏用户分享单个文件
driver.find_element_by_class_name("collect").click()
time.sleep(3)
