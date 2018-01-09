#encoding=utf-8
from flask import Flask,request,abort,make_response,jsonify,session
import json

app = Flask(__name__)

@app.route("/",methods=["post"])
def index():
    # 获取查询字符串的数据
    a=request.args.get("a") #获取同名参数的一个值
    b=request.args.get("b")

    # 获取请求头数据
    content_type = request.headers.get("Content-Type")
    print("content_type=%s"%content_type)

    # 获取请求体的数据
    # 1.普通表单格式的字符串
    # c = request.form.get("c")
    # d = request.form.get("d")

    # print("c=%s"%c)
    # print("d=%s"%d)

    # 2.json格式的字符串
    # 方式一：如果请求头中Content-Type不是application/json 通过这种方法
    # request.data中包含了最原始的请求体数据
    # json_str = request.data

    # print("json_str=%s"%json_str)

    # # 将json字符串转换为字典
    # body_dict = json.loads(json_str)
    # c = body_dict.get("c")
    # d = body_dict.get("d")

    # print("c=%s"%c)
    # print("d=%s"%d)

    # 方式二：flask提供的获取json数据的简便方法 get_json
    # 前提条件：要求请求头Content-Type必须指明是application/json
    # get_json 会将请求体的json字符串直接转换为字典返回给我们
    req_dict = request.get_json()
    c = req_dict.get("c")
    d = req_dict.get("d")

    print("c=%s"%c)
    print("d=%s"%d)


    return "index page"

# 自定义错误页面的方式
@app.errorhandler(404)
def handler_404(e):
    """自定义的处理404错误的方法"""
    # e：被flask调用的时候，传入的错误对象
    return u"自定义的404页面：%s"%e


@app.route("/upload",methods=["POST"])
def upload():
    # 通过files属性获取文件数据，返回文件对象
    files_obj = request.files.get("pic")

    # if not files_obj:
    #     abort(400)

    # 通过read方法读取文件内容
    # file_data = files_obj.read()

    # 获取用户上传文件的真实名字：files_obj.filename

    # 在本地创建打开一个新文件，把用户上传的文件内容读取并写入新文件，关闭新文件
    # with open("./"+files_obj.filename,"wb") as new_file:
    #     new_file.write(file_data)

    files_obj.save("./"+files_obj.filename)

    return "upload ok"

@app.route("/uploadnull",methods=["POST"])
def uploadNull():
    files_obj = request.files.get("pic")

    if not files_obj:
        abort(400)

    files_obj.save("./"+files_obj.filename)

    return "test upload null ok"

@app.route("/resmessage")
def resMesage():
    # 构造响应信息的方式
    # 方式一：元组
    # return "index page", 403, [("Content-Type","application/json"),("name","python")]
    # return "index page", 403, {"Content-Type":"application/json","name":"python2"}
    # return "index page", "403 error",{"Content-Type":"application/json","name":"python3"}
    # return "index page", 666,{"Content-Type":"application/json","name":"python2"}
    # return "index page", "999 perfect",{"Content-Type":"application/json","name":"python2"}
    # return "index page", 400
    # return "index page",400

    # 方式二：make_response()方法
    # make_response(响应体) --> 返回响应对象
    resp = make_response("index page 2")
    resp.status = "400 bad request" #响应状态码
    resp.headers["name3"] = "python3" #响应头

    return resp

@app.route("/jsonhandler")
def jsonHandler():
    # data = {
    #     "name":"python",
    #     "age":18
    # }
    # 原始方法将字典数据转换成json数据
    # json_str = json.dumps(data)
    # return json_str
    # return json_str,200,{"Content-Type":"application/json"}
    
    # 等价与django的jsonResponse,把数据转换为json字符串返回，并帮助我们设置响应头Content-Type为application/json
    # return jsonify(data)
    return jsonify(name="python",age=18)

@app.route("/set_cookie")
def set_cookie():
    # 设置cookie的方法
    resp = make_response("set cookie ok")
    resp.set_cookie("itcast","python1")#默认是临时cookie，浏览器关闭即失效

    # 通过max_age指明有效期，单位是秒
    resp.set_cookie("itcast2","python2",max_age=180)

    return resp

# @app.route("/get_cookie")
# def get_cookie():
#     # 获取cookie
#     cookie = request.cookies.get("itcast")
#     return cookie

# @app.route("/del_cookie")
# def del_cookie():
#     resp = make_response("delete cookie ok")
#     resp.delete_cookie("itcast2")
#     return resp

# flask中使用session需要配置secre_key参数
app.config['SECRET_KEY'] = "qwertyuiop" #随机的字符串

@app.route("/login")
def user_msg():
    # 设置session
    session["user_id"] = 12
    session["user_name"] = "zax"

    return "login ok"

@app.route("/user_login")
def user_login():
    # 获取session
    name = session.get("user_name")
    return "welcom %s"%name

if __name__ == '__main__':
    app.run(debug=True)
    