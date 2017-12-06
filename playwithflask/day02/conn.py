#encoding=utf-8
from pymysql import *

def main():
    # 创建Connection连接
    conn = connect(host='localhost',port=3306,database='jing_dong',user='test',password='mysql',charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()
    # 执行insert语句，并返回受影响的行数：添加一条数据
    # 增加
    count = cs1.execute('insert into goods_cates(name) values("丫丫")')
    #打印受影响的行数
    print(count)
    count = cs1.execute('select * from goods_cates')
    print(cs1.fetchall())
    print(cs1.fetchone())


    # count = cs1.execute('insert into goods_cates(name) values("光盘")')
    # print(count)

    # # 更新
    # count = cs1.execute('update goods_cates set name="机械硬盘" where name="硬盘"')
    # # 删除
    # count = cs1.execute('delete from goods_cates where id=6')

    # 提交之前的操作，如果之前已经之执行过多次的execute，那么就都进行提交
    conn.commit()

    # 关闭Cursor对象
    cs1.close()
    # 关闭Connection对象
    conn.close()

if __name__ == '__main__':
    main()


# kk ➜  day02 git:(master) ✗ mysql -u test -pmysql jing_dong -e "select * from goods_cates"
# +----+---------------------+
# | id | name                |
# +----+---------------------+
# |  1 | 华硕                |
# |  2 | 台式机              |
# |  3 | 平板电脑            |
# |  4 | 服务器/工作站       |
# |  5 | 游戏本              |
# |  6 | 笔记本              |
# |  7 | 笔记本配件          |
# |  8 | 超级本              |
# | 16 | 丫丫                |
# +----+---------------------+