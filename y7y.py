#encoding=utf-8
import string

def chartype(ch):
    if ch in string.ascii_lowercase: return '小写字母'
    elif ch in string.ascii_uppercase: return '大写字母'
    elif ch in string.digits: return '数字'
    else:
        return '其他字符'
def iterchtypecount(s):
    counter = {}
    for c in s:
        counter.setdefault(chartype(c),[]).append(c)
    for t,lst in counter.items():
        yield t, len(lst)

def tongji():
    for chtype,cnts in iterchtypecount(input("请输入字符：")):
        yield(chtype,cnts)
def main():
    for x in tongji():
        print(x)

if __name__=="__main__":
    
    main()