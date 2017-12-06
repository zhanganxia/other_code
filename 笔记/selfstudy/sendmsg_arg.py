# encoding=utf-8
import requests
import sys


if __name__ == '__main__':
    
    phonenum = sys.argv[1]
    send_msg = sys.argv[2]
    print(phonenum,send_msg)
# phonenum = input("请输入手机号:")
# send_msg = input("请输入发送内容:")


# #登录
content = '''
<?xml version="1.0" encoding="UTF-8"?><request><Username>admin</Username><Password>YWRtaW4=</Password></request>
'''
r = requests.post("http://192.168.8.1/api/user/login",data = content.encode("utf-8"))
print(r.text)


#发送短信
content = '''<?xml version="1.0" encoding="UTF-8"?>
<request>
    <Index>-1</Index>
    <Phones>
        <Phone>%s</Phone>
    </Phones>
    <Sca></Sca>
    <Content>%s</Content>
    <Length>2</Length>
    <Reserved>0</Reserved>
    <Date>2017-11-04 22:25:04</Date>
</request>
'''%(phonenum,send_msg)



r = requests.post("http://192.168.8.1/api/sms/send-sms",data = content.encode("utf-8"))
print(r.text)
