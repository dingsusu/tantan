import datetime

from django.core.cache import cache
from django.db.models import Q

from common import keys, errors
from social.models import Swiped, Friend
from tantan import config
from user.models import User,Profile


def get_read_list(uid):

    now = datetime.datetime.now()
    # uid = request/.uid
    user = User.objects.get(id=uid)

    max_birth_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age

    swiped_list = Swiped.objects.filter(uid=uid).only('sid')

    sid_list = [s.sid for s in swiped_list]

    sid_list.append(uid)

    users = User.objects.filter(location=user.profile.dating_location,birthday__range=[
        datetime.date(year=min_birth_year,month=user.birthday.month,day=user.birthday.day),
        datetime.date(year=max_birth_year, month=user.birthday.month, day=user.birthday.day)
    ],gender=user.profile.dating_gender).exclude(id__in=sid_list)[:20]

    data = [user.to_dict() for user in users]
    return data


def like(uid,sid):
    Swiped.like(uid,sid)
    if Swiped.has_like(uid=sid,sid=uid):
        Friend.make_friends(uid,sid)
        return True
    return False


def dislike(uid,sid):

    Swiped.dislike(uid=uid, sid=sid)
    Friend.delete_friend(uid, sid)
    return '解除好友关系'


def superlike(uid,sid):
    Swiped.superlike(uid,sid)
    if Swiped.has_like(uid=sid,sid=uid):
        Friend.make_friends(uid,sid)
        return True
    return False


def rewind(uid):
    key = keys.REWIND % uid
    cached_rewind_times = cache.get(key, 0)
    print(cached_rewind_times)
    if cached_rewind_times < config.MAX_REWIND_TIMES:
        record = Swiped.objects.filter(uid=uid).latest('time')
        record.delete()

        if Friend.is_friend(uid1=uid, uid2=record.sid):
            Friend.delete_friend(uid1=uid, uid2=record.sid)
        record.delete()

        cached_rewind_times += 1
        now = datetime.datetime.now()
        timeout = 86400 - (3600 * now.hour + 60 * now.minute + now.second)
        cache.set(key, cached_rewind_times, timeout)
        return True

    else:
        raise errors.ExceedMaximumRewindTimes



def show_friends(uid):
    friends = Friend.objects.filter(Q(uid1=uid) | Q(uid2=uid))
    friends_id = []
    for i in friends:
        if i.uid1 == uid:
            friends_id.append(i.uid2)
        else:
            friends_id.append(i.uid2)


    users = User.objects.filter(id__in=friends_id)

    data = [user.to_dict() for user in users]
    return data







