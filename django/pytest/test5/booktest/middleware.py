from django.http import HttpResponse

class my_mid:
    def __init__(self):
        print('-------------init')

    def process_request(self,request):
        print('-------request')

    def process_view(self,request,view_func,view_args,view_kwargs):
        print('-------view')

    def process_template_response(self,request,response):
        print('-------template')
        return response

    def process_response(self,request,response):
        print('-------response')
        return response

exclude_ips = ['172.16.179.131']
class BlockIPsMiddleware(object):
    '''中间件类'''
    def process_view(self,request,view_func,*view_args,**view_kwargs):

        '''中间件函数'''
        user_ip = request.META['REMOTE_ADDR'] #获取用户访问IP
        if user_ip in exclude_ips:
            return HttpResponse('<h1>禁止访问</h1>')