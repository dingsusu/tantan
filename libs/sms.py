import random
import json


from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# from tantan.config import ACCESS_KEY_ID,ACCESS_KEY_SECRET
from django.core.cache import cache

from common import keys
from worker import celery_app

ACCESS_KEY_ID = 'LTAI4GCjVxuFenXezkuuHMR2'
ACCESS_KEY_SECRET = 'Hg0LB004d44fskCPw0fr540u1rhJcg'



class SMS:
    def __init__(self,signName,templateCode):
        self.signName = signName  # 签名
        self.templateCode = templateCode  # 模板code
        self.client = client = AcsClient(self.ACCESS_KEY_ID,
                                         self.ACCESS_KEY_SECRET, 'cn-hangzhou')

    def get_vcode(self,size=4):
        start = 10 ** (size - 1)
        end = 10 ** size - 1
        return str(random.randint(start, end))

    @celery_app.task
    def send_sms(self,phone):
        vcode=self.get_vcode()
        print(vcode)
        code_dict={'code':vcode}

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', self.signName)
        request.add_query_param('TemplateCode', self.templateCode)
        request.add_query_param('TemplateParam', json.dumps(code_dict))

        response = self.client.do_action_with_exception(request)
        # python2:  print(response)

        key=keys.VCODE % phone
        timeout=86400 if settings.DEBUG else 900
        print(key)
        cache.set(key,vcode,timeout=timeout)

        result = json.loads(response,encoding='utf-8')
        code=result.get('Code')
        if code == "OK":
            return result
        return False

