#encoding=utf-8
import time
from flask import Flask,request,abort
import hashlib  #python标准库，里面提供sha1 md5 sha256等加密方法
import xmltodict

WECHAT_TOKEN = "itcast" #常量

app = Flask(__name__)

# 第一请求：是微信服务器发起的验证请求
# GET /wechat
@app.route("/wechat8012",methods=["GET","POST"])
def wechat():
    '''处理微信公众号的请求'''
    # 验证请求是否来自微信
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")

    # 按照微信指明的方式，计算签名值
    # 1. 将token，timestamp,nonce三个参数进行字典排序
    li = [WECHAT_TOKEN,timestamp,nonce]
    li.sort()#对于数据是字符串类型，按照字典序排序

    # 2.将三个参数字符串平成一个字符串
    tmp_str = "".join(li)

    # 3.进行sha1加密计算
    hash_obj= hashlib.sha1(tmp_str)
    sign = hash_obj.hexdigest()#获取计算后的结果

    # 4.对比自己计算的sign值与请求中的signature值，如果相同，证明请求来自微信，否则非法
    if sign != signature:
        # 表示请求不是微信
        abort(403)        
    if request.method == "GET":
        
        # 按照微信的说明，为了响应微信的验证请求，需要把微信请求中的echostr参数原样返回，微信就会认可我们的服务器程序
        echostr = request.args.get("echostr")
        return echostr
    else:
        # post
        # 获取请求体xml消息数据
        xml_str = request.data
        # 解析xml
        xml_dict = xmltodict.parse(xml_str)
        req_dict = xml_dict["xml"]

        # 取出消息类型
        msg_type = req_dict["MsgType"]

        if msg_type == "text":
            # 表示文本类型消息
            # 构造回复的消息
            resp_dict = {
                "xml": {
                    "ToUserName":req_dict.get("FromUserName"),
                    "FromUserName":req_dict.get("ToUserName"),
                    "CreateTime":int(time.time()),
                    "MsgType":"text",
                    "Content":req_dict.get("Content")
                }
            }
        else:
            resp_dict = {
                "xml": {
                    "ToUserName":req_dict.get("FromUserName"),
                    "FromUserName":req_dict.get("ToUserName"),
                    "CreateTime":int(time.time()),
                    "MsgType":"text",
                    "Content":"hello welcome!"
                }
            }
            
        # 决定返回的xml数据
        xml_resp_str = xmltodict.unparse(resp_dict)
        return xml_resp_str            
if __name__ == '__main__':
    app.run(port=8012,debug=True)
    
