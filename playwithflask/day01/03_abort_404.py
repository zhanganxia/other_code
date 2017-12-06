from flask import Flask
from flask import abort

app = Flask(__name__)

def load_user(id):
    if int(id) > 10:
        return True
    else:
        return False
    
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello,%s</h1>'% id

if __name__ == '__main__':
    app.run(debug=True)
    
