import re

# *
obj = re.match("h.*h","hsahhh")
if obj:
    print(obj.group())
else:
    print("匹配失败")

# +
obj = re.match("h+","hhh")
if obj:
    print(obj.group())
else:
    print("匹配失败")

# ?
obj = re.match("h?","hhh")
if obj:
    print(obj.group())
else:
    print("匹配失败")

# {m}
obj = re.match("h{3}","hhh")
if obj:
    print(obj.group())
else:
    print("匹配失败")

