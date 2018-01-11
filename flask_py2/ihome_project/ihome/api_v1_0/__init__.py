#encoding=utf-8

from flask import Blueprint

api = Blueprint("api_v1_0",__name__)

from . import users,houses,orders,verify_code