#添加文件用例实例
#判断当前文件个数，登录与退出实例参考本文件下的login.py，这里只给出关注用户分享的逻辑代码

#判断当前的文件个数
inputs=driver.find_elements_by_tag_name('input')
ns=0
for ii in inputs:
    if ii.get_attribute('type')=="checkbox":
        ns=ns+1
print u"当前列表文件为%d"%ns

#判断执行收藏文件之后比收藏之间文件+1，否则抛出异常
if ns==n+1
    print "ok!"
else:
    raise NameError('添加文件失败！！')