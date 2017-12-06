#encoding=utf-8
#一个简单的数据库

people = {
    'Alice':{
        'phone': '2341',
        'addr': 'test'
    },

    'Beth':{
        'phone':'1234',
        'addr':'test2'
    },

    'Cecil':{
        'phone':'3158',
        'addr':'test3'
    }
}

lables = {
    'phone':'phone number',
    'addr':'address'
}
name = input('Name:')

if request == 'p':
    key = 'phone'
if request == 'a':
    key = 'addr'

#如果名字是字典中的有效键才打印
if name in people :
    print ("'%s's %s is %s." %\(name,lables[key],people[name][key]) )
