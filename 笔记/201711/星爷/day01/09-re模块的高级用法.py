import re

#查找指定数据
obj = re.search("\d+","草莓有18盒")
if obj:
    print(obj.group())
else:
    print("匹配失败")

#查找多个,返回列表
result = re.findall("\d+","草莓10颗,苹果5个,葡萄5串")
print(result)

#替换
result = re.sub("\d+","66","草莓10颗,苹果5个,葡萄5串")
print(result)

#定义替换功能的函数
def show_msg(obj):
    #获取匹配结果
    result = obj.group()
    print(result)
    return "你好" + result
result = re.sub("\d+",show_msg,"我有12本书")
print(result)

#正则分割
mystr = input("请输入字符串:")
result = re.split(":|.,",mystr)
print(result)
