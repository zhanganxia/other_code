from flask import Flask,render_template
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)

moment = Moment(app)
#...
@app.route('/')
def index():
    return render_template('index.html',current_time = datetime.utcnow())

@app.route('/name/<name>')
def ext_base():
    return render_template('extends_base.html')


if __name__ == '__main__':
    app.run(debug=True)
    