#encoding=utf-8
from flask import Flask,request,render_template
import urllib2
import json

WECHAT_APPID = "wxa401712a4f50cc75"
WECHAT_SECRET = "e0f5cd4b2a1c793f9760b9a5a7f26ccc"

app = Flask(__name__)

# GET /wechat8012/index?code=xxx
@app.route("/wechat8012/index")
def index():
    # 获取code参数
    code = request.args.get("code")
    # 获取access_token
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(WECHAT_APPID,WECHAT_SECRET,code)
    
    # 使用urllib2发起请求,返回响应对象
    response = urllib2.urlopen(url)

    # 读取响应体的数据
    json_str = response.read()
    resp_dict = json.loads(json_str)

    if "errcode" in resp_dict:
        # 表示微信出错
        return "获取access_token失败"
    access_token = resp_dict.get("access_token")
    user_openid = resp_dict.get("openid")

    # 获取用户的数据
    url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token,user_openid)
    
    # 使用urllib2发起请求,返回响应对象
    response = urllib2.urlopen(url)

    # 读取响应体的数据
    json_str = response.read()
    resp_dict = json.loads(json_str)

    if "errcode" in resp_dict:
        # 表示微信出错
        return "获取用户数据失败"
    # 获取用户数据成功
    return render_template("index.html",user=resp_dict)

if __name__ == '__main__':
    app.run(port=8012,debug=True)
    