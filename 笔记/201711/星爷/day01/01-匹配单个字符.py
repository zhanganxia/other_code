import re

# .
obj = re.match("ha.ha","hahha")
if obj:
    print(obj.group())
else:
    print("匹配失败")
# []
obj = re.match("ha[0-3]ha","ha8ha")
if obj:
    print(obj.group())
else:
    print("匹配失败")

#\d
obj = re.match("\d","123d")
if obj:
    print(obj.group())
else:
    print("匹配失败")

#\D
obj = re.match("\D","哈d#23d")
if obj:
    print(obj.group())
else:
    print("匹配失败")

#\s
obj = re.match("\s","   哈d#23d")
if obj:
    print(obj.group())
else:
    print("匹配失败")

#\S
obj = re.match("\S",".哈d#23d")
if obj:
    print(obj.group())
else:
    print("匹配失败")


