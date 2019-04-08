from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#用户表
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unionid = db.Column(db.String(255))
    create_at = db.Column(db.DateTime,default=datetime.now())



#文件表
class Files(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255),nullable=False)
    status = db.Column(db.Integer,default=0,nullable=False)
    create_at = db.Column(db.DateTime,default=datetime.now())


    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='Files.user_id == User.id', backref='files')


#订单表
class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qrcode = db.Column(db.String(255))
    status = db.Column(db.Integer,default=0,nullable=False)
    create_at = db.Column(db.DateTime,default=datetime.now())


    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='Orders.user_id == User.id', backref='orders')
    file = db.relationship('Files', primaryjoin='Orders.file_id == Files.id', backref='orders')

