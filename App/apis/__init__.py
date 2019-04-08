from flask_restful import Api

from App.apis.FilesApi import File_, getFile_
from App.apis.Login1Api import Login2
from App.apis.LoginApi import Login
from App.apis.OrderApi import Order_, getOrder_

api = Api()

#需要注意  api的初始化 要和init方法联系 否则无法初始化


def init_apis(app):

    api.init_app(app=app)

#网页登录
api.add_resource(Login,'/api/user/login/<code>/')
#小程序登录
# api.add_resource(Login1,'/api/user/login1/<code>/')
api.add_resource(Login2,'/api/user/login1/')

#存储文件信息
api.add_resource(File_,'/api/add/file/path/')

#获取文件列表
api.add_resource(getFile_,'/api/get/files/user/<user_id>/')

#添加订单
api.add_resource(Order_,'/api/add/order/')
#获取订单
api.add_resource(getOrder_,'/api/get/orders/<user_id>/')


