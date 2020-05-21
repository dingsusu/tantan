from qiniu import Auth
from qiniu import put_file, etag,put_data


from worker import celery_app
import qiniu.config
#需要填写你的 Access Key 和 Secret Key


access_key = '9FynT3SHgW1vI9VA-_FO6_uciYbi3WSpvnzvkemP'
secret_key = 'y3b2dpj3EFBR8hgaWDbpUZgoFpTAsGQrMl3Oenjh'
#构建鉴权对象



@celery_app.task
def storage_img(file_data):
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'leijushiwu'
    #上传后保存的文件名
    # key = 'my-python-logo.png'
    #生成上传 Token，可以指定过期时间等

    token = q.upload_token(bucket_name, None, 300000)
    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'

    ret, info = put_data(token, None, file_data)
    # print(info)
    # print(ret)
    if info.status_code == 200:
        return ret.get('key')
    else:
        raise Exception('上传失败')