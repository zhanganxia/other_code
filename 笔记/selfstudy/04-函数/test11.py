result = []
def test(a,begin,end):
    global result
    if begin == end:
        print(a)
        result.append(a[:])
        return
    i = begin
    for num in range(begin,end):
        if a[num] not in a[i:num]:
            a[i],a[num] = a[num],a[i]
            test(a,begin + 1,end)
            a[i],a[num] = a[num],a[i]
test([1,2,2],0,3)
print('result:',result)