import re

# \. 把正则表示中的特殊代码转成普通字符 
obj = re.match("[a-zA-Z0-9_]{4,20}@163\.com$","hello@163.com")
if obj:
    print(obj.group())
else:
    print("匹配失败")

#匹配电话号码,不考虑号段
# "1\d{10}"
#匹配电话号码,指定号段
# "1[34578]\d{9}"

#匹配座机号码0310-2828565 
obj = re.match("0[1-9]\d{1,2}-?[1-8]\d{6,7}","0310-2828565")
if obj:
    print(obj.group())
else:
    print("匹配失败")

print("哈哈哈哈哈")

#匹配 #嘻嘻# 话题
obj = re.match("#[\w]+#","####hahah#")
if obj:
    print(obj.group())
else:
    print("匹配失败")






