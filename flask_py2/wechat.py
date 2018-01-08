#encoding=utf-8
from flask import Flask,request,abort
import hashlib  #python标准库，里面提供sha1 md5 sha256等加密方法

WECHAT_TOKEN = "itcast"

app = Flask(__name__)

# 第一请求：是微信服务器发起的验证请求
# GET /wechat
@app.route("/wechat8012")
def wechat():
    '''处理微信公众号的请求'''
    # 验证请求是否来自微信
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")

    # 按照微信指明的方式，计算签名值
    # 1. 将token，timestamp,nonce三个参数进行字典排序
    li = [WECHAT_TOKEN,timestamp,nonce]
    li.sort()

    # 2.将三个参数字符串平成一个字符串
    tmp_str = "".join(li)

    # 3.进行sha1加密计算
    hash_obj= hashlib.sha1(tmp_str)
    sign = hash_obj.hexdigest()#获取计算后的结果

    # 4.对比自己计算的sign值与请求中的signature值，如果相同，证明请求成功
    if sign != signature:
        # 表示请求不是微信
        abort(403)
    
    # 按照威信的说明，为了响应微信的验证请求，需要把微信请求中的
    echostr = request.args.get("echostr")
    return echostr

if __name__ == '__main__':
    app.run(port=8012,debug=True)
    
