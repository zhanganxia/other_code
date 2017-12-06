from flask import Flask,render_template
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField,SubmitField
from wtforms.validators import Required

app = Flask(__name__)
#为了实现CSRF保护，Flask-WTF需要程序设置一个密钥
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        #？？？
        name = form.name.data
        form.name.data = ''
    return render_template('index.html',form = form,name = name,current_time = datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)
    