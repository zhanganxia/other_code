#进行调试，日志的输出等级
#notice:1  waring:2  error:3
def level(level):    
    def yanzhen(func):
        def inner(*args,**kwargs):
            if level == 1:
                print("输出提示信息")
            elif level == 2:
                print("输出警告信息")
            else:
                print("输出错误信息")                                
            print("信息验证中...")
            msg = func(*args,**kwargs)
            print("*********验证结束*********")
            #return msg
        return inner
    return yanzhen

@level(2)
def login(username):
    #return "%s您的信息正在验证请稍后..." %username
    print("%s，您的信息正在验证请稍后..."%username)

@level(2)
def register(idcast,addr):
    print("正在验证您的身份信息,%s,%s，请稍后..."%(idcast,addr))
   
login("zax")
register("123456","陕西")