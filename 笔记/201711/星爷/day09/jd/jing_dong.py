from pymysql import * 
from hashlib import *
#import hashlib
import time

class JD(object):
    
    def __init__(self):
        self.conn = connect(host="localhost",
                     user="test",
                     password="mysql",
                     database="jing_dong",
                     port=3306,
                     charset='utf8')
        self.cur = self.conn.cursor()
        self.customer_id = None

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def opt_menu(self):
        print("----------京东商城---------------")
        print("操作选项：")
        print("1:查看所有商品信息")
        print("2:下订单")
        print("3:登录")
        print("4:注册")
        print("5:退出")
        opt = input("请输入功能选项：")

        return opt

    def run(self):
        while True:
            opt = self.opt_menu()
            if opt == "1":
                self.select()
            elif opt == "2":
                self.take_order()
            elif opt == "3":
                self.login()
            elif opt == "4":
                self.register()
            elif opt == "5":
                break
            else:
                print("请输入正确的选项！")       
    def select(self):
        """显示所有商品信息"""

        sql = """select g.id,g.name,c.name,b.name,g.price from goods as g
                inner join goods_cates as c on g.cate_name = c.id
                inner join goods_brands as b on g.brand_name = b.id"""
        ret = self.cur.execute(sql)
        ret = self.cur.fetchall()
        for item in ret:
            print(item) 

    def register(self):

        name = input("请输入用户名：")
        pwd = input("请输入密码:")
        tel = input("请输入电话号码：")
        sha = sha1()
        sha.update(pwd.encode())
        sha_pwd = sha.hexdigest()
        print(sha_pwd)

        #在注册之前应该先判断用户名是否已经被注册
        sql = "select * from customer where name = %s"
        ret = self.cur.execute(sql,name)
        if ret:
            print("******用户名已使用，请重新选择操作！*******")
            return
        sql = "insert into customer (name,password,tel) values (%s,%s,%s)"
        ret = self.cur.execute(sql,(name,sha_pwd,tel))
        self.conn.commit()    

    def login(self):
        name = input("请输入登录用户名：")
        pwd = input("请输入登录密码：") 

        #sha1对密码进行加密
        sha = sha1()
        sha.update(pwd.encode())
        sha_pwd = sha.hexdigest()

        #在登录之前判断此用户是否存在
        sql = "select * from customer where name= %s and password = %s"
        self.cur.execute(sql,(name,sha_pwd))
        ret = self.cur.fetchone()
        print(ret)
        if not ret:
            print("用户不存在请重新输入...")
            return
        #执行到这里用户是一定存在的
        print("恭喜你登录成功",ret[1]) 
        #获取用户的id
        self.customer_id = ret[0]

    def take_order(self):
        #判断用户是否登录
        if not self.customer_id:
            print("下订单前请先登录")
            return

        #显示商品信息
        self.select()

        #获取商品编号
        goods_id = input("请输入商品编号：")

        #判断商品是否存在
        if not goods_id.isdigit():
            print("请输入正确的商品编号！")
            return
        #生成订单，操作orders表
        #time.strptime(str,fmt='%a %b %d %H:%M:%S %Y')
        #根据fmt的格式把一个字符串解析为时间元组
        #time.strftime(fmt[,tupletime]):接收以时间元组，并返回可读字符串表示当地时间，格式由fmt决定
        order_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into orders (order_data_time,customer_id) values ('%s','%s')"%(order_time,self.customer_id)
        self.cur.execute(sql)

        order_id = self.cur.lastrowid
        print("order_id的类型是",type(order_id))

        #生成订单详情，数量默认为1
        sql = "insert into orders_detail (order_id,goods_id,quantity) values ('%s','%s','1')"%(order_id,goods_id)
        self.cur.execute(sql)

        self.conn.commit()
        print("订单已经生成")

def main():
    jingd = JD()

    jingd.run()

if __name__ == '__main__':
    main()
    