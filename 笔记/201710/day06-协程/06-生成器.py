#生成器是一个特殊的迭代器,那么也就是说可以使用next函数获取下一个值
g = (x * 2 for x in range(3))
print(g)

result = next(g)
print(result)

result = next(g)
print(result)

result = next(g)
print(result)