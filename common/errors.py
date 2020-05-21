PHONE_ERROR = 1000
SEND_VCODE_ERROR = 1001
VCODE_ERROR = 1002
PROFILE_ERROR = 1003
LOGIN_REQUIRED = 1004
AVATAR_ERROR = 1005
EXCEED_MAXIMUM_REWIND_TIMES = 1006




class LogicErr(Exception):
    code = None
    data = None

def gen_logic_err(name,code,data):
    return type(name,(LogicErr,),{'code':code,'data':data})


PHONEERROR = gen_logic_err('PhoneError',code=1000,data='手机号码格式错误')
SENDVCODEERROR = gen_logic_err('SendVcodeError',code=1001,data='发送手机验证码错误')
VcodeError = gen_logic_err('VcodeError', code=1002, data='短信验证错误')
ProfileError = gen_logic_err('ProfileError', 1003, '个人交友资料错误')
LoginRequired = gen_logic_err('LoginRequired', 1004, '请登录')
ExceedMaximumRewindTimes = gen_logic_err('ExceedMaximumRewindTimes', 1005, '超过当日最大反悔次数')
PermissonDenied = gen_logic_err('PermissonDenied', 1006, '权限不足, 请充值')
AVATARERROR = gen_logic_err('AvatarError',code=1007,data='头像上传失败')