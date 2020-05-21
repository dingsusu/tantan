import re

# from django.shortcuts import render
from celery.result import AsyncResult
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from libs.http import render_json
from common import errors
from libs.qiniuyun_ import storage_img
from libs import sms

from common import keys
from user.models import User,Profile
from user import forms
from tantan import config
from worker import celery_app


def submit_phone(request):

    phone=request.POST.get('phone')
    result=re.match(r'^1[33456789]\d{9}',phone)
    print(phone)
    if not result:
        print('*****')
        return errors.PHONEERROR

    # if __name__ == '__main':
    # sms=SMS(signName='类聚识物',templateCode='SMS_189836899')
    res=sms.send_sms.delay(phone)
    print(res)
    if res:
        return render_json()





@require_http_methods(['POST'])
def submin_vcode(request):
    phone =  request.POST.get('phone')
    vcode = request.POST.get('vcode')

    key = keys.VCODE % phone
    cached_vcode = cache.get(key)

    print(key,cached_vcode)
    if vcode and (vcode == cached_vcode):
        # try:
        #     user = User.objects.filter(phonenum=phone)
        # except User.DoesNotExist as e:
        #     user = User.objects.create(phonenum=phone,nickname=phone)
        user, _  = User.objects.get_or_create(phonenum=phone,defaults={'nickname':phone})
        request.session['uid']=user.id
        return render_json(data=user.to_dict(exclude='id',))
    else:
        return render_json(code=errors.VCODE_ERROR,data='code is wrong')


def get_profile(request):
    uid = request.uid
    user = User.objects.get(id=uid)

    return render_json(user.profile.to_dict(exclude='id',))

def edit_profile(request):


    user_form = forms.UserForm(request.POST)
    profile_form = forms.ProfileForm(request.POST)

    if not profile_form.is_valid() or not user_form.is_valid()  :
        form_error = {}
        form_error.update(**user_form.errors)
        form_error.update(**profile_form.errors)
        return render_json(code=errors.PROFILE_ERROR,data=form_error)

    uid = request.uid

    User.objects.filter(id=uid).update(**user_form.cleaned_data)

    Profile.objects.update_or_create(id=uid,defaults=profile_form.cleaned_data)
    return render_json()




def upload_avatar(request):
    uid = request.uid

    filename = keys.AVATAR % request.uid
    image_file = request.FILES.get('avatar')

    if image_file is None:
        return render_json(code= errors.AVATAR_ERROR, data='未上传图片')

    image_data=image_file.read()

    try:
        file_name = storage_img.delay(image_data).get()


    except Exception as e:
        return render_json(code= errors.AVATAR_ERROR, data='上传失败1',)

    try:

        avatar_url = config.avatar_url + file_name
        User.objects.filter(id=uid).update(avatar=avatar_url)
        return render_json(code=0, data=avatar_url)

    except Exception as e:
        print(e)
        return render_json(code= errors.AVATAR_ERROR, data='上传失败',)

