# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse

from App.models import Seller


class SellerLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='phone', type=str)
        parser.add_argument(name='password', type=str)
        parse = parser.parse_args()
        phone = parse.get('phone')
        password = parse.get('password')
        seller = Seller.query.filter(Seller.phone==phone,Seller.password==password).first()
        if seller:
            data = {
                'id':seller.id,
                'name':seller.name,
                'phone':seller.phone,
                'password':seller.password,
                'longitude':seller.longitude,
                'latitude':seller.latitude,
                'province':seller.province,
                'city':seller.city,
                'area':seller.area,
                'detail':seller.detail,
                'create_at':seller.create_at.strftime('%Y/%m/%d')
            }
            return jsonify(data)
        else:
            return jsonify({'err':'用户不存在'})
