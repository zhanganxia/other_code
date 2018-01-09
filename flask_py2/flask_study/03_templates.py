#encoding=utf-8

from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo

app = Flask(__name__)

# 使用wtform扩展，需要配置secret_key
app.config["SECRET_KEY"] = "aaaasssddd"

@app.route("/")
def index():
    # 方式一
    # user_name = "python"
    # user_age = 18
    # # 渲染模板
    # return render_template('index.html',name=user_name,age=user_age)

    # 方式二:使用字典（对字典解包，传递数据）
    data = {
        "name":"python",
        "age":18,
        "a_list":[1,2,3,4,5,6],
        "a_dict":{'a':100},
        "a_str":" hello python "
    } 
    return render_template('hello3.html',**data)

# 自定义过滤器
# 方式一：
def handle_list_step2(a_list):
    # a_list:代表要处理的模板变量，而且还要有一个返回值(放到模板变量的位置)
    return a_list[::2]    
#注册过滤器
app.add_template_filter(handle_list_step2,"list2")

# 方式二：
@app.template_filter("list3")
def handle_list_step3(a_list):
    return a_list[::3]


# 定义表单类
class RegisterForm(FlaskForm):
    '''注册表单'''
    # validators指明对这个字段的验证行为
    user_name = StringField(label=u"用户名",validators=[DataRequired(u'用户名不能为空')])
    password = PasswordField(label=u"密码",validators=[DataRequired(u"密码不能为空")])
    password2 = PasswordField(label=u"重复密码",validators=[DataRequired(u"确认密码不能为空"),EqualTo("password",u"两次密码不一致")])
    submit = SubmitField(label=u"提交注册")

@app.route("/register",methods=["GET","POST"])
def register():
    # 创建表单对象
    form = RegisterForm()
    if request.method == "GET":
        return render_template("hello3.html",form=form)
    else:
        # 对应post方式提交表单
        # 创建的表单对象中包含了用户提交的数据
        # 验证表单的数据validate_on_submit
        # 如果用户的数据满足我们声明的全部验证行为，返回真，否则返回假
        if form.validate_on_submit():
            # 表示条件满足
            # 提取表单数据
            uname = form.user_name.data
            password = form.password.data
            password2 = form.password2.data

            print(uname,password,password2)
            return "register OK"
        else:
            return render_template("hello3.html",form=form)
if __name__ == '__main__':
    app.run(debug=True)
    