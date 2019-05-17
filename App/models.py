# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#用户表
class Carousel(db.Model):
    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cover_img = db.Column(db.String(255),nullable=False)


#用户表
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unionid = db.Column(db.String(255))
    openid = db.Column(db.String(255))
    head_img = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


#商家表
class Seller(db.Model):
    __tablename__ = 'seller'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11),nullable=False)
    name = db.Column(db.String(64),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    longitude = db.Column(db.String(255),nullable=False)
    latitude = db.Column(db.String(255),nullable=False)
    province = db.Column(db.String(46),nullable=False)
    city = db.Column(db.String(46),nullable=False)
    area = db.Column(db.String(46),nullable=False)
    detail = db.Column(db.String(255),nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


#文件表
class Files(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255),nullable=False)
    status = db.Column(db.Integer,default=0,nullable=False)
    page = db.Column(db.Integer,nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='Files.user_id == User.id', backref='files')


#订单表
class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # qrcode = db.Column(db.String(255))
    code = db.Column(db.String(255),nullable=False)
    number = db.Column(db.Integer,default=0,nullable=False)
    type = db.Column(db.String(64),nullable=False)
    payType = db.Column(db.String(64),nullable=False)
    paperType = db.Column(db.String(64),nullable=False)
    price = db.Column(db.Float,default=0,nullable=False)
    order_no = db.Column(db.String(255),nullable=False)
    status = db.Column(db.Integer,default=0,nullable=False)
    is_save = db.Column(db.Integer,default=0,nullable=False)
    is_idcard = db.Column(db.Integer,default=0,nullable=False)
    payStatus = db.Column(db.Integer,default=0,nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    pickDate = db.Column(db.DateTime)
    remark = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    # file_id = db.Column(db.Integer, db.ForeignKey('files.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    file_id = db.Column(db.String(255),nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='Orders.user_id == User.id', backref='orders')
    # file = db.relationship('Files', primaryjoin='Orders.file_id == Files.id', backref='orders')
    seller = db.relationship('Seller', primaryjoin='Orders.seller_id == Seller.id', backref='orders')

