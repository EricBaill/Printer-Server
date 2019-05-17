# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource

from App.models import Carousel


class getCarousels(Resource):
    def get(self):
        banners = Carousel.query.all()
        if len(banners) >= 3:
            data = [{
                'id':banners[-1].id,
                'cover_img':banners[-1].cover_img,
                },
                {
                    'id': banners[-2].id,
                    'cover_img': banners[-2].cover_img,
                },
                {
                    'id': banners[-3].id,
                    'cover_img': banners[-3].cover_img,
                }]
            return jsonify(data)
        elif len(banners) == 2:
            data = [{
                'id': banners[-1].id,
                'cover_img': banners[-1].cover_img,
                },
                {
                    'id': banners[-2].id,
                    'cover_img': banners[-2].cover_img,
                }]
            return jsonify(data)
        elif len(banners) == 1:
            data = [{
                'id': banners[0].id,
                'cover_img': banners[0].cover_img,
            }]
            return jsonify(data)
        else:
            return jsonify([])




