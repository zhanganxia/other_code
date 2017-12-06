from pymysql import * 

def insert():
    #1.创建数据库连接
    # host=None, user=None, password="",
    # database=None, port=0, unix_socket=None,
    # charset='',
    conn = connect(host="localhost", 
                  user="test",
                  password="mysql",
                  database="jing_dong",
                  port=3306,
                  charset='utf8')

    #2.获取数据库的cursor对象
    cur = conn.cursor()
    #3.编写sql语句
    #增  sql = "insert into goods_cates (name) values ('Apple')"
    #改  sql = "update goods_cates set name = '电话' where id=26"
    sql = "delete from goods_cates where id = 25;"
    #4.执行sql语句
    cur.execute(sql)

    #5.对于数据更新操作不会立即影响到源数据
    #如果希望能够更新到数据库需要使用commit
    conn.commit()
    #6.关闭cursor，connction
    cur.close()
    conn.close()

def main():
    insert()

if __name__ == '__main__':
    main()
    