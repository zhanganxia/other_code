# encoding=utf-8
from werkzeug.routing import BaseConverter


# 自定义正则转换器
class ReConverter(BaseConverter):
    """自定义正则转换器"""
    def __init__(self,url_map,regex):
        super(ReConverter,self).__init__(url_map)
        self.regex = regex