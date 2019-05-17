# -*- coding: utf-8 -*-
import requests
from flask import jsonify
from flask_restful import Resource, reqparse

from App.models import Seller, db


#管理端
class Seller_(Resource):
    def get(self,seller_id):
        seller = Seller.query.filter(Seller.id==seller_id).first()
        if seller:
            data = {
                'id':seller.id,
                'name':seller.name,
                'password':seller.password,
                'longitude':seller.longitude,
                'latitude':seller.latitude,
                'phone': seller.phone,
                'province':seller.province,
                'city':seller.city,
                'area':seller.area,
                'detail':seller.detail,
                'create_at':seller.create_at.strftime('%Y/%m/%d')
            }
            return jsonify(data)
        else:
            return jsonify({})


class addSeller(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='name', type=str)
        parser.add_argument(name='phone', type=str)
        parser.add_argument(name='password', type=str)
        parser.add_argument(name='province', type=str)
        parser.add_argument(name='city', type=str)
        parser.add_argument(name='area', type=str)
        parser.add_argument(name='detail', type=str)
        parse = parser.parse_args()
        name = parse.get('name')
        phone = parse.get('phone')
        password = parse.get('password')
        province = parse.get('province')
        city = parse.get('city')
        area = parse.get('area')
        detail = parse.get('detail')
        start = province + city + area + detail
        url = "http://api.map.baidu.com/geocoder?address=" + start + "&output=json&ak=GPccFSSW7vYUNcSpoKCzzGNsRxNGGyf1"
        response = requests.get(url)
        answer = response.json()
        longitude = answer['result']['location']['lng']
        latitude = answer['result']['location']['lat']

        seller = Seller()
        seller.name = name
        seller.phone = phone
        seller.password = password
        seller.longitude = longitude
        seller.latitude = latitude
        seller.province = province
        seller.city = city
        seller.area = area
        seller.detail = detail
        db.session.add(seller)
        db.session.commit()
        return jsonify({'msg':'添加成功'})


class putSeller(Resource):
    def put(self,seller_id):
        parser = reqparse.RequestParser()
        parser.add_argument(name='name', type=str)
        parser.add_argument(name='phone', type=str)
        parser.add_argument(name='password', type=str)
        parser.add_argument(name='province', type=str)
        parser.add_argument(name='city', type=str)
        parser.add_argument(name='area', type=str)
        parser.add_argument(name='detail', type=str)
        parse = parser.parse_args()
        name = parse.get('name')
        phone = parse.get('phone')
        password = parse.get('password')
        province = parse.get('province')
        city = parse.get('city')
        area = parse.get('area')
        detail = parse.get('detail')

        start = province + city + area + detail
        print(start)

        url = "http://api.map.baidu.com/geocoder?address=" + start + "&output=json&ak=GPccFSSW7vYUNcSpoKCzzGNsRxNGGyf1"
        response = requests.get(url)
        answer = response.json()
        longitude = answer['result']['location']['lng']
        latitude = answer['result']['location']['lat']

        print(longitude)
        print(latitude)

        seller = Seller.query.filter(Seller.id==seller_id).first()
        print(seller_id)
        print(seller)
        if seller:
            seller.name = name
            seller.phone = phone
            seller.password = password
            seller.longitude = longitude
            seller.latitude = latitude
            seller.province = province
            seller.city = city
            seller.area = area
            seller.detail = detail
            db.session.commit()
            return jsonify({'msg':'修改成功'})
        else:
            return jsonify({})


class delSeller(Resource):
    def delete(self,seller_id):
        seller = Seller.query.filter(Seller.id==seller_id).first()
        if seller:
            db.session.delete(seller)
            db.session.commit()


#手机端
class getSellers(Resource):
    def get(self):
        list_ = []
        sellers = Seller.query.all()
        if sellers:
            for seller in sellers:
                data = {
                    'id':seller.id,
                    'name':seller.name,
                    'password':seller.password,
                    'longitude':seller.longitude,
                    'latitude':seller.latitude,
                    'province':seller.province,
                    'phone':seller.phone,
                    'city':seller.city,
                    'area':seller.area,
                    'detail':seller.detail,
                    'create_at':seller.create_at.strftime('%Y/%m/%d')
                }
                list_.append(data)
            return jsonify(list_)
        else:
            return jsonify([])


class searchSellers(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='name', type=str)
        parse = parser.parse_args()
        name = parse.get('name')
        list_ = []
        sellers = Seller.query.filter(Seller.name.like('%'+name+'%')).all()
        if sellers:
            for seller in sellers:
                data = {
                    'id':seller.id,
                    'name':seller.name,
                    'password':seller.password,
                    'longitude':seller.longitude,
                    'latitude':seller.latitude,
                    'province':seller.province,
                    'phone': seller.phone,
                    'city':seller.city,
                    'area':seller.area,
                    'detail':seller.detail,
                    'create_at':seller.create_at.strftime('%Y/%m/%d')
                }
                list_.append(data)
            return jsonify(list_)
        else:
            return jsonify([])