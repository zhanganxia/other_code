1.cookie和session的比较
    Session是在服务端保存的一个数据结构，用来跟踪用户的状态，这个数据可以保存在集群、数据库、文件中；
    Cookie是客户端保存用户信息的一种机制，用来记录用户的一些信息，也是实现Session的一种方式

2. session操作：
    1）设置session:HttpRequest对象.session['键']=‘值’
    2）获取session:HttpRequest对象.session.get('键')
    3）设置session对应的cookie过期时间：HttpRequest对象.


通过method属性获取当前请求的方式，得到的是“GET”或者“post”字符串


4. 模板中解析变量的过程：比如:obj.name
