#coding=utf-8

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid= '8a216da860e4d4f10160e869839500f4'

# 主帐号Token
accountToken= '8a59416aff1843ecbccfcb7aed34a791'

# 应用ID
appId='8a216da860e4d4f10160e86983f300fb'

# 请求地址，格式如下，不需要写http：//
serverIP='app.cloopen.com'

# 请求端口
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为列表 例如：["12","34"],如不需要替换请填''
  # @param $tempId 模板Id

# def sendTemplateSMS(to,datas,tempId):
    
    
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
    
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems(): 
        
#         if k=='templateSMS' :
#                 for k,s in v.iteritems(): 
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


class CCP(object):
    """"自己封装的发送短信的辅助类"""
    # 用来保存对象的类属性
    instance = None

    def __new__(cls):
        # 判断CCP类有没有已经创建好的对象，如果没有，创建一个对象，并且保存
        # 如果有，则将保存的对象直接返回
        if cls.instance is None:
            obj = super(CCP,cls).__new__(cls)

            # 初始化REST SDK
            obj.rest = REST(serverIP,serverPort,softVersion)
            obj.rest.setAccount(accountSid,accountToken)
            obj.rest.setAppId(appId)

            cls.instance = obj
        return cls.instance

    def send_template_sms(self,to,datas,temp_id):
        result = self.rest.sendTemplateSMS(to,datas,temp_id)
        # for k,v in result.iteritems(): 
            
        #     if k=='templateSMS' :
        #         for k,s in v.iteritems(): 
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        # result = self.rest.sendTemplateSMS(to,datas,temp_id)
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送短信成功，0表示没有出现任何异常，如果失败，返回负值
            return 0
        else:
            # 表示发送短信失败
            return -1

#sendTemplateSMS(手机号码，内容数据，模板ID)
if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms("18218366324",["1234",5],1)

# 运行此文件测试结果：

# 这是请求的URL：
# https://app.cloopen.com:8883/2013-12-26/Accounts/8a216da860e4d4f10160e869839500f4/SMS/TemplateSMS?sig=A16D35298DCBD93A037D409CA50B34C4
# 这是请求包体:
# <?xml version="1.0" encoding="utf-8"?><SubAccount><datas><data>1234</data><data>5</data></datas><to>18218366324</to><templateId>1</templateId><appId>8a216da860e4d4f10160e86983f300fb</appId>            </SubAccount>            
# 这是响应包体:
# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <Response>
#     <statusCode>000000</statusCode>
#     <TemplateSMS>
#         <smsMessageSid>5d6a2d3b796e47068a231945a2d0f7cd</smsMessageSid>
#         <dateCreated>20180112162417</dateCreated>
#     </TemplateSMS>
# </Response>

# ********************************
# smsMessageSid:5d6a2d3b796e47068a231945a2d0f7cd
# dateCreated:20180112162417
# statusCode:000000

    
