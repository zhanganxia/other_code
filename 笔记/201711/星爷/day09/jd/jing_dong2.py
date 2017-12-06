from pymysql import * 
from hashlib import *

class JD(object):
    
    def __init__(self):
        self.conn = connect(host="localhost",
                        user = "test",
                        password = "mysql",
                        database = "jing_dong",
                        port = 3306,
                        charset = "utf8")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def menu(self):
        print("**********京东商城*********")
        print("请输入选项：")
        print("1.查看商品信息")
        print("2.下订单")
        print("3.登录")
        print("4.注册")
        print("5.退出")
        
        opt = input("请输入功能选项:")
        return opt

    def select_goods(self):
        sql = """select g.id,g.name,c.name,b.name,g.price from goods as g
            inner join goods_cates as c on g.cate_name = c.id 
            inner join goods_brands as b on g.brand_name = b.id"""
        ret = self.cur.execute(sql)
        ret = self.cur.fetchall()
        for temp in ret:
            print(temp)

    def login(self):
        name = input("请输入用户名:")
        pwd = input("请输入密码:")

        #判断用户在数据库中是否存在
        sql = "select * from customer where name = '%s' and password = '%s'"%(name,pwd)       
        self.cur.execute(sql)
        ret = self.cur.fetchone()
        if not ret:
            print("用户不存在，请重新输入！")
            return
        
        #执行到这里说明用户是存在的
        print("恭喜你登录成功：",ret[1])

        customer_id = ret[0]

    def register(self):
        name = input("请输入要注册的用户名：")
        pwd = input("请输入注册密码：")
        tel = input("请输入电话号码：")

        sha = sha1()
        sha.update(pwd.encode())
        sha_pwd = sha.hexdigest()
        print(sha_pwd)

        #判断用户在数据库中是否存在
        sql = "select * from customer where name = '%s' and password = '%s' "%(name,sha_pwd)
        self.cur.execute(sql)
        ret = self.cur.fetchone()
        if ret:
            print("用户已存在，请重新输入！")
            return
        #执行到这里，输入的用户名在数据库中是不存在的
        sql = "insert into customer (name,password,tel) values ('%s','%s','%s')"%(name,sha_pwd,tel)
        self.cur.execute(sql)
        self.conn.commit()

    def run(self):
        while True:
            opt = self.menu()
            if opt == "1":
                self.select_goods()
            elif opt == "2":
                pass
            elif opt == "3":
                self.login()
            elif opt == "4":
                self.register()
            elif opt == "5":
                break
            else:
                print("请输入正确的功能选项")
                
def main():
    jing_d = JD()
    jing_d.run()

if __name__ == '__main__':
    main()
    