from django.utils.deprecation import MiddlewareMixin

from libs.http import render_json
from common import errors
from common.errors import LogicErr



class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        white_list = ['/api/user/vcode/submit/phone',
                      '/api/user/submit/vcode/']

        if request.path in white_list:
            return None

        uid = request.session.get('uid')
        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED,data='请登录')
        request.uid=uid



class LogicErrMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # 只捕获逻辑错误异常
        if isinstance(exception, LogicErr):
            # 可以捕获.
            # 直接返回response
            return render_json(code=exception.code, data=exception.data)
