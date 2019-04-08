# -*- coding: utf-8 -*-
import time

from flask import jsonify
from flask_restful import Resource, reqparse

from App.models import Orders, db, Files


class Order_(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='user_id', type=int)
        parser.add_argument(name='id', type=int)
        parse = parser.parse_args()
        user_id = parse.get('user_id')
        file_id = parse.get('id')

        f = Files.query.filter(Files.id==file_id).first()
        t = time.time()
        qrcode = f.content + str(int(t))

        order = Orders()
        order.user_id = user_id
        order.qrcode = qrcode
        order.file_id = file_id
        db.session.add(order)
        db.session.commit()

        order = Orders.query.order_by(db.desc(Orders.id),Orders.user_id==user_id,Orders.file_id==file_id).first()
        if order:
            file = Files.query.filter(Files.id==order.file_id).first()
            if file:
                data = {
                    'id':order.id,
                    'status':order.status,
                    'create_at':order.create_at,
                    'qrcode':order.qrcode,
                    'files':{
                        'id':file.id,
                        'content':file.content
                    }
                }
                return jsonify(data)
            else:
                return jsonify({})
        else:
            return jsonify({})


class getOrder_(Resource):
    def get(self,user_id):
        list_ = []
        print(user_id)
        orders = Orders.query.filter(Orders.user_id==user_id).all()
        if orders:
            for order in orders:
                file = Files.query.filter(Files.id == order.file_id).first()
                if file:
                    data = {
                        'id': order.id,
                        'status': order.status,
                        'create_at': order.create_at,
                        'qrcode': order.qrcode,
                        'files': {
                            'id': file.id,
                            'content': file.content
                        }
                    }
                    list_.append(data)
                    print(list_)
                else:
                    pass
            return jsonify(list_)
        else:
            return jsonify([])
