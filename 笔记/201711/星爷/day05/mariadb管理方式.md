# mariadb 管理方式 identified by

只有root权限有添加/删除数据库的权限

ctrl+a（ahead）：命令行行首
ctrl+e （end）：命令行行尾


#数据库结构
实例-->库-->表-->字段-->数据

## 启动
systemctl start mariadb

## 关闭
systemctl stop mariadb

## 查看状态
systemctl status mariadb


#退出mariadb 
ctrl + d

#mariadb 用户名密码
test   mysql

#使用test用户登录
mysql -u test -p(回车)

#查看数据库
show databases;

#切换库 
use test

#创建表（要设置id自增长就需要设置这个键为主键（primary key）;）
CREATE TABLE test1(
user_id INT NOT NULL AUTO_INCREMENT,
user_name VARCHAR(100) NOT NULL,
password VARCHAR(40) NOT NULL,
address VARCHAR(100) NOT NULL,
PRIMARY KEY (user_id)
);


#添加数据
INSERT INTO test1 (user_id,user_name,password,address) VALUES (1,"zax","123456","深圳");

#查看字符集
SHOW VARIABLES LIKE 'character%';


#创建数据库字符集为utf-8
UTF-8: CREATE DATABASE `test2` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


#使用root用户给普通用户分配看数据库的权限
#-->grant all 分配所有权限
#-->test2.*   test2数据库下的所有表
GRANT ALL ON test2.* TO 'test'@'localhost' WITH GRANT OPTION;


#修改数据库服务器的字符集
1.root权限下 vi /etc/my.cnf 

2.在[mysqld]字段里加入 character-set-server=utf8


#数据精度
decimal（4，1）-->小数点前最多4位，小数点后面最多一位


http://download1.navicat.com/download/navicat120_mysql_en_x64.tar.gz





























