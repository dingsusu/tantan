from django.utils.deprecation import MiddlewareMixin

from libs.http import render_json
from common import errors


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