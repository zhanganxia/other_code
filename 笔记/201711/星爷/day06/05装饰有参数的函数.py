def yanzhen(func):
    def inner(username):
        print("登录验证中...")
        func(username)
        print("验证结束")
    return inner

@yanzhen
def login(username):
    print("%s，您的信息正在验证请稍后..."%username)

login("zax")