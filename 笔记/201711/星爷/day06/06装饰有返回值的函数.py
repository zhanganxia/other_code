def yanzhen(func):
    def inner(username):
        print("登录验证中...")
        ret = func(username)
        print(ret)
        print("验证结束")
        print("1111111111")
        return ret
    return inner

@yanzhen
def login(username):
    return "%s您的信息正在验证请稍后..." %username
    #print("%s，您的信息正在验证请稍后..."%username)

ret = login("zax")
print(ret)