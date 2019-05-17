# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource

from App.models import Orders, db


class Notify(Resource):
    def get(self):
        order = Orders.query.order_by(db.desc(Orders.id)).first()
        if order:
            order.payStatus = 1
            db.session.commit()
            print('ok')
            return jsonify({'msg':'ok'})
        else:
            return jsonify({})