# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse
from qiniu import Auth


class Token(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='key', type=str)
        parse = parser.parse_args()
        key = parse.get('key')
        # 需要填写你的 Access Key 和 Secret Key
        ak = "x8Wiq7iIUk3mZnuKDG2A5y14HLIHieMYZK3UsJJT"
        sk = "sYQit3y31B9VIL-vQkUho9toQn0noLcf-UFihcQZ"
        # 构建鉴权对象
        q = Auth(ak, sk)
        # 要上传的空间
        bucket_name = 'cloudprint'
        # 上传到七牛后保存的文件名
        key = key
        policy = {}
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, key, 3600, policy)
        data = {
            'token':token
        }
        print(token)
        return jsonify(data)
