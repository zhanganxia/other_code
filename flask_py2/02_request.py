#encoding=utf-8
from flask import Flask,request
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

@app.route("/upload",methods=["POST"])
def upload():
    # 通过files属性获取文件数据，返回文件对象
    files_obj = request.files.get("pic")

    # 通过read方法读取文件内容
    file_data = files_obj.read()

    # 获取用户上传文件的真实名字

    # 在本地创建打开一个新文件，把用户上传的文件内容读取并写入新文件，关闭新文件
    with open("./demo.png","wb") as new_file:
        new_file.write(file_data)

    return "upload ok"
if __name__ == '__main__':
    app.run(debug=True)
    