from redis import StrictRedis

if __name__ == '__main__':
    try:    
        # 创建StrictRedis对象，用于连接redis服务器
        sr = StrictRedis(host='localhost',port=6379,db=0)
        
        # 添加一个String类型的元素，key:name val:zax
        # result = sr.set('name','zax')
        # print(result)

        # 修改name的值为ljq
        # result = sr.set('name','ljq')
        # print(result)

        # 获取name的值
        # result = sr.get('name')
        # print(result)

        # 删除name和它的值
        # result = sr.delete('name')
        # print(result)

        # 获取数据库中所有的key
        result = sr.keys()
        print(result)
    except Exception as e:
        print(e)


