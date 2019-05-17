# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource

from App.models import User


class getUser(Resource):
    def get(self,user_id):
        user = User.query.filter(User.id==user_id).first()
        if user:
            data = {
                'id':user.id,
                'nickName':user.nickname,
                'avatarUrl':user.head_img,
            }
            return jsonify(data)
        else:
            return jsonify({})