# -*- coding: utf-8 -*-
import datetime
import shutil
import time
import os
import zipfile
from urllib.request import urlretrieve
from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy import and_, extract
from App.models import Orders, db, Files, Seller
from qiniu import Auth, put_file


class Order_(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='user_id', type=int)
        parser.add_argument(name='file_id', type=str)
        parser.add_argument(name='seller_id', type=int)
        parser.add_argument(name='type', type=str)
        parser.add_argument(name='payType', type=str)
        parser.add_argument(name='paperType', type=str)
        parser.add_argument(name='pickDate', type=str)
        parser.add_argument(name='remark', type=str)
        parser.add_argument(name='copiesNumber', type=str)
        parser.add_argument(name='is_idcard', type=int)
        parser.add_argument(name='is_save', type=int)
        parser.add_argument(name='price', type=int)
        parse = parser.parse_args()
        user_id = parse.get('user_id')
        file_id = parse.get('file_id')
        seller_id = parse.get('seller_id')
        type_ = parse.get('type')
        payType = parse.get('payType')
        paperType = parse.get('paperType')
        pickDate = parse.get('pickDate')
        remark = parse.get('remark')
        copiesNumber = parse.get('copiesNumber')
        is_idcard = parse.get('is_idcard')
        is_save = parse.get('is_save')
        price = parse.get('price')

        t = time.time()
        order_no = str(int(t))
        code = str(int(t))

        order = Orders()
        order.user_id = user_id
        order.file_id = file_id
        order.seller_id = seller_id
        order.order_no = order_no
        order.code = code
        order.is_idcard = is_idcard
        order.is_save = is_save
        order.price = price
        order.type = type_
        order.payType = payType
        order.paperType = paperType
        order.pickDate = pickDate
        order.number = copiesNumber
        order.remark = remark
        db.session.add(order)
        db.session.commit()

        list_ = []
        order = Orders.query.order_by(db.desc(Orders.id)).first()
        if order:
            fileIds = eval(order.file_id)
            for f_id in fileIds:
                file = Files.query.filter(Files.id==f_id).first()
                seller = Seller.query.filter(Seller.id==order.seller_id).first()
                if file and seller:
                    data = {
                        'id':order.id,
                        'order_no':order.order_no,
                        'code':order.code,
                        'type':order.type,
                        'payType':order.payType,
                        'paperType':order.paperType,
                        'pickDate':order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                        'remark':order.remark,
                        'status':order.status,
                        'copiesNumber':order.number,
                        'create_at':order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                        # 'qrcode':order.qrcode,
                        'files':{
                            'id':file.id,
                            'content':file.content
                        },
                        'seller':{
                            'id':seller.id,
                            'name':seller.name
                        }
                    }
                    list_.append(data)
            list2 = []
            for i in range(len(list_)):
                if list_[i] != {}:
                    order_list = []
                    order_list.append(list_[i].get('files'))
                    for j in range(i + 1, len(list_)):
                        if list_[i].get('id') == list_[j].get('id'):
                            order_list.append(list_[j].get('files'))
                            list_[i]['files'] = order_list
                            list_[j] = {}

                    list2.append(list_[i])
            for k in list2:
                if isinstance(k['files'], dict):
                    list_k = []
                    list_k.append(k['files'])
                    k['files'] = list_k
            return jsonify(list2)
        else:
            return jsonify([])


class getOrder_(Resource):
    def get(self,user_id):
        list_ = []
        orders = Orders.query.filter(Orders.user_id==user_id).all()
        if orders:
            for order in orders:
                fileIds = eval(order.file_id)
                for f_id in fileIds:
                    file = Files.query.filter(Files.id == f_id).first()
                    seller = Seller.query.filter(Seller.id == order.seller_id).first()
                    if file and seller:
                        data = {
                            'id': order.id,
                            'order_no': order.order_no,
                            'code': order.code,
                            'type': order.type,
                            'payType': order.payType,
                            'paperType': order.paperType,
                            'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                            'remark': order.remark,
                            'status': order.status,
                            'copiesNumber': order.number,
                            'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                            # 'qrcode':order.qrcode,
                            'files': {
                                'id': file.id,
                                'content': file.content
                            },
                            'seller': {
                                'id': seller.id,
                                'name': seller.name
                            }
                        }
                        list_.append(data)
            list2 = []
            for i in range(len(list_)):
                if list_[i] != {}:
                    order_list = []
                    order_list.append(list_[i].get('files'))
                    for j in range(i + 1, len(list_)):
                        if list_[i].get('id') == list_[j].get('id'):
                            order_list.append(list_[j].get('files'))
                            list_[i]['files'] = order_list
                            list_[j] = {}

                    list2.append(list_[i])
            for k in list2:
                if isinstance(k['files'], dict):
                    list_k = []
                    list_k.append(k['files'])
                    k['files'] = list_k
            return jsonify(list2)
        else:
            return jsonify([])


class SellerOrder(Resource):
    def get(self,seller_id):
        list_ = []
        orders = Orders.query.filter(Orders.seller_id==seller_id).all()
        if orders:
            for order in orders:
                fileIds = eval(order.file_id)
                # for f_id in fileIds:
                file = Files.query.filter(Files.id == fileIds[-1]).first()
                seller = Seller.query.filter(Seller.id == order.seller_id).first()
                if file and seller:
                    data = {
                        'id': order.id,
                        'order_no': order.order_no,
                        'code': order.code,
                        'type': order.type,
                        'payType': order.payType,
                        'paperType': order.paperType,
                        'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                        'remark': order.remark,
                        'status': order.status,
                        'copiesNumber': order.number,
                        'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                        # 'qrcode':order.qrcode,
                        'files': {
                            'id': file.id,
                            'content': file.content
                        },
                        'seller': {
                            'id': seller.id,
                            'name': seller.name
                        }
                    }
                    list_.append(data)
            list2 = []
            for i in range(len(list_)):
                if list_[i] != {}:
                    order_list = []
                    order_list.append(list_[i].get('files'))
                    for j in range(i + 1, len(list_)):
                        if list_[i].get('id') == list_[j].get('id'):
                            order_list.append(list_[j].get('files'))
                            list_[i]['files'] = order_list
                            list_[j] = {}

                    list2.append(list_[i])
            for k in list2:
                if isinstance(k['files'], dict):
                    list_k = []
                    list_k.append(k['files'])
                    k['files'] = list_k
            return jsonify(list2)
        else:
            return jsonify([])


class orderInfo(Resource):
    def get(self,order_id):
        order = Orders.query.filter(Orders.id==order_id).first()
        list_ = []
        if order:
            IdCard = order.is_idcard
            if IdCard == 0:
                fileIds = eval(order.file_id)
                file = Files.query.filter(Files.id == fileIds[-1]).first()
                seller = Seller.query.filter(Seller.id==order.seller_id).first()
                if file and seller:
                    data = {
                        'id': order.id,
                        'order_no': order.order_no,
                        'code': order.code,
                        'type': order.type,
                        'payType': order.payType,
                        'paperType': order.paperType,
                        'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                        'remark': order.remark,
                        'status': order.status,
                        'payStatus': order.payStatus,
                        'copiesNumber': order.number,
                        'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                        'name': seller.name,
                        #'qrcode':order.qrcode,
                        'files': [{
                            'id': file.id,
                            'content': file.content,
                            'create_at': file.create_at.strftime('%Y/%m/%d %H:%M:%S')
                        }]
                    }
                    list_.append(data)
                return jsonify(list_)

            elif IdCard == 1:
                fileIds = eval(order.file_id)
                if len(fileIds) != 3:
                    file1 = Files.query.filter(Files.id == fileIds[0]).first()
                    file2 = Files.query.filter(Files.id == fileIds[1]).first()

                    # 通过地址下载图片
                    os.makedirs('./img/', exist_ok=True)
                    IMAGE_URL = 'https://www.jianxinshanghai.com/' + file1.content
                    urlretrieve(IMAGE_URL, './img/' + 'img' + '1' + '.png')

                    os.makedirs('./img/', exist_ok=True)
                    IMAGE_URL = 'https://www.jianxinshanghai.com/' + file2.content
                    urlretrieve(IMAGE_URL, './img/' + 'img' + '2' + '.png')

                    input_path = "./img"
                    output_path = './zip'
                    output_name = order.code + '.zip'
                    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
                    filelists = []
                    files = os.listdir(input_path)
                    for file in files:
                        if os.path.isdir(input_path + '/' + file):
                            filelists.append(input_path + '/' + filelists)
                        else:
                            filelists.append(input_path + '/' + file)

                    for file in filelists:
                        f.write(file)
                    # 调用了close方法才会保证完成压缩
                    f.close()
                    print(output_path + r"/" + output_name)

                    AK = 'x8Wiq7iIUk3mZnuKDG2A5y14HLIHieMYZK3UsJJT'
                    SK = 'sYQit3y31B9VIL-vQkUho9toQn0noLcf-UFihcQZ'
                    # 要上传的文件夹绝对路径
                    dir = './zip/{}'.format(output_name)

                    bucket_name = 'cloudprint'
                    q = Auth(AK, SK)
                    token = q.upload_token(bucket_name)
                    fpath, fname = os.path.split(dir)
                    patharr = fpath.split('\\')
                    if len(patharr) >= 2:
                        key = '/'.join(patharr[2:]) + 'printer' + '/' + 'files' + '/' + fname
                    else:
                        key = 'printer' + '/' + 'files' + '/' + fname
                    print(key)
                    ret, info = put_file(token, key, dir)
                    print(ret)

                    file_ = Files()
                    file_.user_id = order.user_id
                    file_.page = 1
                    file_.content = key
                    db.session.add(file_)
                    db.session.commit()
                    files = Files.query.all()
                    if files:
                        files_id = files[-1].id

                        order.file_id = str([file1.id,file2.id,files_id])
                        print(order.file_id)
                        db.session.commit()
                    else:
                        pass

                    seller = Seller.query.filter(Seller.id == order.seller_id).first()
                    if seller:
                        data = {
                            'id': order.id,
                            'order_no': order.order_no,
                            'code': order.code,
                            'type': order.type,
                            'payType': order.payType,
                            'paperType': order.paperType,
                            'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                            'remark': order.remark,
                            'status': order.status,
                            'payStatus': order.payStatus,
                            'copiesNumber': order.number,
                            'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                            'name': seller.name,
                            # 'qrcode':order.qrcode,
                            'files': [{
                                'id': files[-1].id,
                                'content': files[-1].content,
                                'create_at': files[-1].create_at.strftime('%Y/%m/%d %H:%M:%S')
                            }]
                        }
                        list_.append(data)

                        # 删除本地存储文件
                        delDir = "./img"
                        delList = list(os.listdir(delDir))
                        for f in delList:
                            filePath = os.path.join(delDir, f)
                            if os.path.isfile(filePath):
                                os.remove(filePath)
                                print(filePath + " was removed!")
                            elif os.path.isdir(filePath):
                                shutil.rmtree(filePath, True)
                            print("Directory: " + filePath + " was removed!")

                        # 删除本地存储文件
                        delDir = "./zip"
                        delList = list(os.listdir(delDir))
                        for f in delList:
                            filePath = os.path.join(delDir, f)
                            if os.path.isfile(filePath):
                                os.remove(filePath)
                                print(filePath + " was removed!")
                            elif os.path.isdir(filePath):
                                shutil.rmtree(filePath, True)
                            print("Directory: " + filePath + " was removed!")
                        return jsonify(list_)

                    else:
                        pass

                elif len(fileIds) == 3:
                    file = Files.query.filter(Files.id == fileIds[-1]).first()
                    seller = Seller.query.filter(Seller.id == order.seller_id).first()
                    if file and seller:
                        data = {
                            'id': order.id,
                            'order_no': order.order_no,
                            'code': order.code,
                            'type': order.type,
                            'payType': order.payType,
                            'paperType': order.paperType,
                            'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                            'remark': order.remark,
                            'status': order.status,
                            'payStatus': order.payStatus,
                            'copiesNumber': order.number,
                            'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                            'name': seller.name,
                            # 'qrcode':order.qrcode,
                            'files': [{
                                'id': file.id,
                                'content': file.content,
                                'create_at': file.create_at.strftime('%Y/%m/%d %H:%M:%S')
                            }]
                        }
                        list_.append(data)
                        return jsonify(list_)
                    else:
                        return jsonify([])
                else:
                    return jsonify([])
            else:
                pass
        else:
            return jsonify([])


class orderIncome(Resource):
    def get(self,seller_id):
        list_ = []
        orders = Orders.query.filter(Orders.seller_id == seller_id,Orders.status==1).all()
        if orders:
            for order in orders:
                data = {
                    'id': order.id,
                    'order_no': order.order_no,
                    'code': order.code,
                    'type': order.type,
                    'payType': order.payType,
                    'paperType': order.paperType,
                    'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                    'remark': order.remark,
                    'status': order.status,
                    'payStatus': order.payStatus,
                    'copiesNumber': order.number,
                    'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                    # 'qrcode':order.qrcode,
                }
                list_.append(data)
            return jsonify(list_)
        else:
            return jsonify([])


class getDayOrders(Resource):
    def get(self,seller_id):
        list_ = []
        year_ = datetime.datetime.now().year
        month_ = datetime.datetime.now().month
        day_ = datetime.datetime.now().day

        orders = Orders.query.filter(Orders.seller_id==seller_id,and_(
            extract('year', Orders.create_at) == year_,
            extract('month', Orders.create_at) == month_,
            extract('day', Orders.create_at) == day_,
        )).all()

        if orders:
            for order in orders:
                data = {
                    'id':order.id,
                    'order_no':order.order_no,
                    'code':order.code,
                    'type':order.type,
                    'payType':order.payType,
                    'paperType':order.paperType,
                    'pickDate':order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                    'remark':order.remark,
                    'copiesNumber': order.number,
                    'payStatus': order.payStatus,
                    'status':order.status,
                    'create_at':order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                    # 'qrcode':order.qrcode,
                }
                list_.append(data)
            return jsonify(list_)
        else:
            return jsonify([])


class orderUnpaid(Resource):
    def get(self,seller_id):
        list_ = []
        orders = Orders.query.filter(Orders.seller_id == seller_id,Orders.status==0).all()
        if orders:
            for order in orders:
                data = {
                    'id': order.id,
                    'order_no': order.order_no,
                    'code': order.code,
                    'type': order.type,
                    'payType': order.payType,
                    'paperType': order.paperType,
                    'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                    'remark': order.remark,
                    'copiesNumber': order.number,
                    'status': order.status,
                    'payStatus': order.payStatus,
                    'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                    # 'qrcode':order.qrcode,
                }
                list_.append(data)
            return jsonify(list_)
        else:
            return jsonify([])


class putStatus(Resource):
    def get(self,order_id):
        order = Orders.query.filter(Orders.id==order_id).first()
        if order:
            order.status = 1
            db.session.commit()
            return jsonify({'msg':'已取件'})
        else:
            return jsonify({})


class searchOrder(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='code', type=str)
        parse = parser.parse_args()
        code = parse.get('code')
        order = Orders.query.filter(Orders.code==code).first()
        if order:
            fileIds = eval(order.file_id)
            file = Files.query.filter(Files.id == fileIds[-1]).first()
            if file:
                data = [{
                    'id': order.id,
                    'order_no': order.order_no,
                    'code': order.code,
                    'type': order.type,
                    'payType': order.payType,
                    'paperType': order.paperType,
                    'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                    'remark': order.remark,
                    'status': order.status,
                    'copiesNumber': order.number,
                    'payStatus': order.payStatus,
                    'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                    # 'qrcode':order.qrcode,
                    'files': [{
                        'id': file.id,
                        'content': file.content
                    }]
                }]
                return jsonify(data)
        else:
            return jsonify([])


class orderData(Resource):
    def get(self,seller_id):
        list_ = []
        orders = Orders.query.filter(Orders.seller_id==seller_id).order_by(db.desc(Orders.id)).all()
        if orders:
            for order in orders:
                fileIds = eval(order.file_id)
                file = Files.query.filter(Files.id == fileIds[-1]).first()
                if file:
                    data = {
                        'id': order.id,
                        'order_no': order.order_no,
                        'code': order.code,
                        'type': order.type,
                        'payType': order.payType,
                        'paperType': order.paperType,
                        'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                        'remark': order.remark,
                        'copiesNumber': order.number,
                        'status': order.status,
                        'payStatus': order.payStatus,
                        'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                        # 'qrcode':order.qrcode,
                        'files': [{
                            'id': file.id,
                            'content': file.content
                        }]
                    }
                    list_.append(data)
            return jsonify(list_)
        else:
            return jsonify([])


class getStatus(Resource):
    def get(self,seller_id,status):
        list_ = []
        orders = Orders.query.filter(Orders.seller_id==seller_id,Orders.status==status).all()
        if orders:
            for order in orders:
                fileIds = eval(order.file_id)
                file = Files.query.filter(Files.id == fileIds[-1]).first()
                seller = Seller.query.filter(Seller.id == order.seller_id).first()
                if file and seller:
                    data = {
                        'id': order.id,
                        'order_no': order.order_no,
                        'code': order.code,
                        'type': order.type,
                        'payType': order.payType,
                        'paperType': order.paperType,
                        'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                        'remark': order.remark,
                        'status': order.status,
                        'payStatus': order.payStatus,
                        'copiesNumber': order.number,
                        'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                        'name': seller.name,
                        # 'qrcode':order.qrcode,
                        'files': {
                            'id': file.id,
                            'content': file.content,
                            'create_at': file.create_at.strftime('%Y/%m/%d %H:%M:%S')
                        }
                    }
                    list_.append(data)
            list2 = []
            for i in range(len(list_)):
                if list_[i] != {}:
                    order_list = []
                    order_list.append(list_[i].get('files'))
                    for j in range(i + 1, len(list_)):
                        if list_[i].get('id') == list_[j].get('id'):
                            order_list.append(list_[j].get('files'))
                            list_[i]['files'] = order_list
                            list_[j] = {}

                    list2.append(list_[i])
            for k in list2:
                if isinstance(k['files'], dict):
                    list_k = []
                    list_k.append(k['files'])
                    k['files'] = list_k
            return jsonify(list2)
        else:
            return jsonify([])


class sellerOrderInfo(Resource):
    def get(self,order_id):
        order = Orders.query.filter(Orders.id==order_id).first()
        list_ = []
        if order:
            fileIds = eval(order.file_id)
            file = Files.query.filter(Files.id == fileIds[-1]).first()
            seller = Seller.query.filter(Seller.id==order.seller_id).first()
            if file and seller:
                data = {
                    'id': order.id,
                    'order_no': order.order_no,
                    'code': order.code,
                    'type': order.type,
                    'payType': order.payType,
                    'paperType': order.paperType,
                    'pickDate': order.pickDate.strftime('%Y/%m/%d %H:%M:%S'),
                    'remark': order.remark,
                    'status': order.status,
                    'payStatus': order.payStatus,
                    'copiesNumber': order.number,
                    'create_at': order.create_at.strftime('%Y/%m/%d %H:%M:%S'),
                    'name': seller.name,
                    #'qrcode':order.qrcode,
                    'files': [{
                        'id': file.id,
                        'content': file.content,
                        'create_at': file.create_at.strftime('%Y/%m/%d %H:%M:%S')
                    }]
                }
                list_.append(data)
                return jsonify(list_)
            else:
                return jsonify([])
        else:
            return jsonify([])