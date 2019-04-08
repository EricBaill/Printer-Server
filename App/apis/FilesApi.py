# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse
from App.models import Files, db


class File_(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='user_id', type=int)
        parser.add_argument(name='path', type=str)
        parse = parser.parse_args()
        user_id = parse.get('user_id')
        path = parse.get('path')

        print(user_id)
        print(path)

        file = Files()
        file.user_id = user_id
        file.content = path
        db.session.add(file)
        db.session.commit()

        file = Files.query.order_by(db.desc(Files.id),Files.user_id==user_id).first()
        if file:
            data = {
                'id':file.id,
                'content':file.content
            }
            return jsonify(data)
        else:
            return jsonify({})

class getFile_(Resource):
    def get(self,user_id):
        list_ = []
        files = Files.query.filter(Files.user_id==user_id).all()
        if files:
            for file in files:
                data = {
                    'id':file.id,
                    'content':file.content,
                    'create_at':file.create_at
                }
                list_.append(data)
            return jsonify(list_)
        else:
            return jsonify([])