from pymysql import * 

def insert():
    conn = connect(host="localhost", 
                  user="test",
                  password="mysql",
                  database="jing_dong",
                  port=3306,
                  charset='utf8')

    #2.获取数据库的cursor对象
    cur = conn.cursor()
    #3.编写sql语句
    sql = "select * from goods_cates"
    #4.执行sql语句
    ret = cur.execute(sql)
    #print(ret)

    #fetchone

    ret = cur.fetchone()
    # print(ret)

    #fetchall()如果没有数据返回，此时数据类型是空元组，如果有数据返回，返回的是一个嵌套的元组
    ret = cur.fetchall()
    #print(ret)
    for item in ret:
        print(item[0])
        print(item[1])

    #5.对于数据更新操作不会立即影响到源数据
    #如果希望能够更新到数据库需要使用commit
    #conn.commit()
    #6.关闭cursor，connction
    cur.close()
    conn.close()

def main():
    insert()

if __name__ == '__main__':
    main()
    