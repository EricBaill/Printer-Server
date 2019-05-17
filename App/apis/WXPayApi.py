# -*- coding: utf-8 -*-
import hashlib
import time
import requests
import xmltodict
from flask import jsonify
from flask_restful import Resource, reqparse
import random
from App.models import User, Orders

parser = reqparse.RequestParser()
parser.add_argument(name='order_id',type=int)


#微信扫码支付
class WXPay(Resource):
    def post(self):
        parse = parser.parse_args()
        order_id = parse.get('order_id')
        order = Orders.query.filter(Orders.id==order_id).first()
        if order:
            user = User.query.filter(User.id==order.user_id).first()
            openid = user.openid

            #生成随机字符串
            chars = "abcdefghijklmnopqrstuvwxyz0123456789"
            strs = []
            for x in range(32):
                strs.append(chars[random.randrange(0, len(chars))])
            nonce_str = "".join(strs)

            #参数配置
            data = {
                'appid': 'wx8f8eae4c7f709a50',  # 小程序id
                'mch_id': '1488536192',  # 商户号
                'nonce_str': nonce_str.upper(),  # 获取随机字符串大写
                'body': 'JSAPI-Pay',  # 商品描述
                'out_trade_no': str(int(time.time())),  # 商户订单号
                'total_fee': int(order.price),  # 商品价格 以分为单位 整数
                'spbill_create_ip': '192.168.1.106',  # 终端ip 通过 socket 获取
                'notify_url': "http://192.168.1.108:5000/api/notify/",  # 支付结果通知地址
                'trade_type': 'JSAPI',  # 交易类型 小程序为 JSAPI
                'openid': openid  # 获取请求参数中的用户openid JSAPI支付必须传
            }

            stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
            stringSignTemp = '{0}&key={1}'.format(stringA, 'nlJWQh9fCcpKXXKyZX1xmkj1gKRKcClo').encode('utf-8')
            sign = hashlib.md5(stringSignTemp).hexdigest()
            data['sign'] = sign.upper() #要大写

            xml = []
            for k in sorted(data.keys()):
                v = data.get(k)
                if k == 'detail' and not v.startswith('<![CDATA['):
                    v = '<![CDATA[{}]]>'.format(v)
                xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
            xmlstr = '<xml>{}</xml>'.format(''.join(xml))

            url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            r = requests.post(url, data=xmlstr,headers={'Content-Type': 'application/xml'})
            #设置字符集防止出现乱码
            xml_str = r.text.encode('ISO-8859-1').decode('utf-8')

            #将xml格式转换成json格式
            json_str = xmltodict.parse(xml_str)

            list_ = json_str
            l = list(list_.values())[0]
            # 生成随机字符串
            chars = "abcdefghijklmnopqrstuvwxyz0123456789"
            strs = []
            for x in range(30):
                strs.append(chars[random.randrange(0, len(chars))])
            nonce_str = "".join(strs)
            package = list(l.values())[7]
            timeStamp = str(int(time.time()))

            data = {
                "appId": 'wx8f8eae4c7f709a50',
                "nonceStr": nonce_str.upper(),
                "package": "prepay_id=" + package,
                "signType": 'MD5',
                "timeStamp": timeStamp,
            }

            stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
            stringSignTemp = '{0}&key={1}'.format(stringA, 'nlJWQh9fCcpKXXKyZX1xmkj1gKRKcClo').encode('utf-8')
            sign = hashlib.md5(stringSignTemp).hexdigest()

            data1 = {
                "appId": 'wx8f8eae4c7f709a50',
                "nonceStr": nonce_str.upper(),
                "prepay_id": "prepay_id=" + package,
                "signType": 'MD5',
                "timeStamp": timeStamp,
                'sign' :sign.upper()
            }

            return data1
        else:
            return jsonify({})

