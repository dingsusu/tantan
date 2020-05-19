import json

from django.http import  HttpResponse

from tantan.settings import DEBUG


def render_json(code=0,data=None):
    data_dict = {
        'code':code,
        'data':data,
    }
    if DEBUG:
        data_dump=json.dumps(data_dict,indent=4,ensure_ascii=False,sort_keys=True)
    else:
        data_dump=json.dumps(data_dict,ensure_ascii=False,separators=[':',','])
    return HttpResponse(data_dump)