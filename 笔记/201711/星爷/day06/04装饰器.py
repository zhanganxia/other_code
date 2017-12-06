def yanzhen(func):
    def inner():
        print("登录验证中...")
        func()
        print("验证结束")
    return inner

@yanzhen
def login():
    print("正在验证请稍后...")

login()