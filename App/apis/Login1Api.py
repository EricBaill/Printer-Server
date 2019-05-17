# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import logging
from flask import jsonify
from flask_restful import Resource, reqparse
import requests

from App.models import User, db

logger = logging.getLogger('Weixin')

import base64
import json
from Crypto.Cipher import AES


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
        print(decrypted)

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

# class Login1(Resource):
#     def get(self,code):
#         url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx2f283376f6a50187&secret=1c0a84c675a5044f1b271953066da3f2&js_code={}&grant_type=authorization_code'.format(
#             code)
#         response = requests.get(url)
#         logger.info('post[%s]=>[%d][%s]' % (
#             code, response.status_code, response.text
#         ))
#
#         resData = response.json()
#         print(resData)
#         openid = resData['openid']
#         print(openid)
#
#         u = User.query.filter(User.openid==openid).first()
#         if u:
#             data = {
#                 'id':u.id
#             }
#             print(data)
#             return jsonify(data)
#         else:
#             user = User()
#             user.openid = openid
#             db.session.add(user)
#             db.session.commit()
#             u1 = User.query.filter(User.openid == openid).first()
#             data = {
#                 'id': u1.id
#             }
#             print(data)
#             return jsonify(data)


class Login_(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='encryptedData', type=str)
        parser.add_argument(name='iv', type=str)
        parser.add_argument(name='code', type=str)
        parser.add_argument(name='nickName', type=str)
        parser.add_argument(name='avatarUrl', type=str)
        parse = parser.parse_args()
        encryptedData = parse.get('encryptedData')
        iv = parse.get('iv')
        code = parse.get('code')
        nickName = parse.get('nickName')
        avatarUrl = parse.get('avatarUrl')

        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx8f8eae4c7f709a50&secret=16e80fdcf5d807af471e2517a1f87b2d&js_code={}&grant_type=authorization_code'.format(
            code)
        response = requests.get(url)
        logger.info('post[%s]=>[%d][%s]' % (
            code, response.status_code, response.text
        ))
        resData = response.json()
        sessionKey = resData['session_key']
        openid = resData['openid']
        appId = 'wx8f8eae4c7f709a50'
        sessionKey = sessionKey
        encryptedData = encryptedData
        iv = iv

        pc = WXBizDataCrypt(appId, sessionKey)

        d = pc.decrypt(encryptedData, iv)
        for k,v in d.items():
            if k == 'unionId':
                unionId = d[k]
            else:
                pass
        unionid = unionId

        u = User.query.filter(User.unionid == unionid).first()
        if u:
            data = {
                'id': u.id
            }
            return jsonify(data)
        else:
            user = User()
            user.unionid = unionid
            user.openid = openid
            user.nickname = nickName
            user.head_img = avatarUrl
            db.session.add(user)
            db.session.commit()
            u1 = User.query.filter(User.unionid == unionid).first()
            data = {
                'id': u1.id
            }
            return jsonify(data)
