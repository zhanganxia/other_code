from flask import Flask
from flask import request

app = Flask(__name__)

#静态路由,地址路径输入:http://127.0.0.1:5000/
@app.route('/')
def index():
    return '<h1>Hello World</h1>'

#动态路由,地址路径输入:http://127.0.0.1:5000/user/zax
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s!</h1>'% name

@app.route('/')
def index2():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>'% user_agent

if __name__ == '__main__':
    app.run(debug=True)
    







