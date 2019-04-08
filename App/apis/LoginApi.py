# -*- coding: utf-8 -*-
import logging

from flask import jsonify
from flask_restful import Resource
import requests

from App.models import User, db

logger = logging.getLogger('Weixin')

class Login(Resource):
    def get(self,code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxc468bfba0f55b4cf&secret=d5df87f7e5784d482bb7eb64d8bc63d8&code={}&grant_type=authorization_code'.format(
            code)
        response = requests.get(url)
        logger.info('post[%s]=>[%d][%s]' % (
            code, response.status_code, response.text
        ))

        resData = response.json()
        access_token = resData['access_token']
        openid = resData['openid']
        print(resData)
        print(openid)

        url1 = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}'.format(access_token, openid)
        response = requests.get(url1)
        logger.info('post[%s]=>[%s][%s][%s]' % (
            access_token, openid, response.status_code, response.text
        ))
        resData = response.json()
        unionid = resData['unionid']

        print(resData)

        u = User.query.filter(User.unionid==unionid).first()
        if u:
            data = {
                'id':u.id
            }
            print(data)
            return jsonify(data)
        else:
            user = User()
            user.unionid = unionid
            db.session.add(user)
            db.session.commit()
            u1 = User.query.filter(User.unionid == unionid).first()
            data = {
                'id': u1.id
            }
            print(data)
            return jsonify(data)
