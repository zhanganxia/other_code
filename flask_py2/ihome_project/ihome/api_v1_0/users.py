#encoding=utf-8
from . import api

@api.route('/register')
def register():
    return "register page"