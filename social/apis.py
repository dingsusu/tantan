import datetime

from common import keys, errors
from libs.http import render_json
from social import logical
from django.core.cache import cache


from social.models import Swiped
from social.models import Friend
from tantan import config


def get_read_list(request):
    uid = request.uid
    data = logical.get_read_list(uid)
    return render_json(data=data)



def like(request):
    sid = int(request.GET.get('sid'))
    uid = request.uid
    flag = logical.like(uid,sid)
    if flag:
        return render_json(data={'matched':True})
    return render_json(data={'matched':False})


def dislike(request):
    sid = int(request.GET.get('sid'))
    uid = request.uid

    data=logical.dislike(uid,sid)
    return render_json(data=data)



def superlike(request):
    sid = int(request.GET.get('sid'))
    uid = request.uid
    flag = logical.superlike(uid,sid)
    if flag:
        return render_json(data={'matched':True})
    return render_json(data={'matched':False})



def rewind(request):
    uid = request.uid
    print(uid)
    if logical.rewind(uid):
        return render_json()

    # else:
    #     return render_json(code = errors.EXCEED_MAXIMUM_REWIND_TIMES,data='超过反悔次数')



def show_friens(request):
    uid = request.uid
    data = logical.show_friends(uid)
    return render_json(data=data)