def yanzhen(func):
    def inner(*args,**kwargs):
        print("信息验证中...")
        msg = func(*args,**kwargs)
        print("*********验证结束*********")
        #return msg
    return inner

@yanzhen
def login(username):
    #return "%s您的信息正在验证请稍后..." %username
    print("%s，您的信息正在验证请稍后..."%username)

@yanzhen
def register(idcast,addr):
    print("正在验证您的身份信息,%s,%s，请稍后..."%(idcast,addr))
   
login("zax")
register("123456","陕西")

