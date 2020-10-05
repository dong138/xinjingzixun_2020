# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'QNUcQDIywEgcP_zvaO0XfDZxwKwpbsbRVXN7BTPe'
secret_key = 'y2PBSlCykoz3PU3du3lt7epERRTbVQQ1HrgW27-G'

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 要上传的空间
bucket_name = 'xinjingzixun2020'


def upload_image_to_qiniu(localfile, key):
    """
    上传图片到七牛云
    :param localfile:要上传的文件路径
    :param key:保存到七牛云之后的文件名
    :return: True表示成功
    """
    # 上传后保存的文件名
    # key = 'my-python-logo.png'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = './bbb.png'

    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    return True


if __name__ == "__main__":
    upload_image_to_qiniu()
