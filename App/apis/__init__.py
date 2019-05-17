# -*- coding: utf-8 -*-

from flask_restful import Api

from App.apis.CarouselApi import getCarousels
from App.apis.FilesApi import File_, getFile_, FileInfo
from App.apis.Login1Api import Login_
from App.apis.LoginApi import Login
from App.apis.NotifyApi import Notify
from App.apis.OrderApi import Order_, getOrder_, SellerOrder, orderInfo, orderIncome, getDayOrders, orderUnpaid, \
    putStatus, searchOrder, orderData, getStatus, sellerOrderInfo
from App.apis.SellerApi import Seller_, putSeller, getSellers, searchSellers, addSeller
from App.apis.SellerLoginApi import SellerLogin
from App.apis.TokenApi import Token
from App.apis.UserApi import getUser
from App.apis.WXPayApi import WXPay

api = Api()

#需要注意  api的初始化 要和init方法联系 否则无法初始化
def init_apis(app):
    api.init_app(app=app)


#网页登录
api.add_resource(Login,'/api/user/login/<code>/')
#小程序登录
# api.add_resource(Login1,'/api/user/login1/<code>/')
api.add_resource(Login_,'/api/user/login1/')

#存储文件信息
api.add_resource(File_,'/api/add/file/path/')
#获取文件列表
api.add_resource(getFile_,'/api/get/files/user/<user_id>/')
#根据文件ID获取文件详情
api.add_resource(FileInfo,'/api/get/file/info/<id>/')

#添加订单
api.add_resource(Order_,'/api/add/order/')
#获取订单
api.add_resource(getOrder_,'/api/get/orders/<user_id>/')


#商家登录
api.add_resource(SellerLogin,'/api/seller/login/')


#根据商家ID获取订单信息
api.add_resource(SellerOrder,'/api/get/seller/orders/<seller_id>/')
#商家获取每日订单信息
api.add_resource(getDayOrders,'/api/get/day/seller/orders/<seller_id>/')
#商家获取未支付金额
api.add_resource(orderUnpaid,'/api/get/seller/unpaid/order/<seller_id>/')
#商家获取订单详情
api.add_resource(sellerOrderInfo,'/api/get/seller/order/massage/<order_id>/')
#用户获取订单详情
api.add_resource(orderInfo,'/api/get/seller/order/infos/<order_id>/')
#收益情况
api.add_resource(orderIncome,'/api/get/seller/order/income/<seller_id>/')
#修改取件状态
api.add_resource(putStatus,'/api/put/order/status/<order_id>/')
#根据取件码搜索订单信息
api.add_resource(searchOrder,'/api/search/order/code/')
#按日期查询订单
api.add_resource(orderData,'/api/get/order/date/<seller_id>/')
#按订单状态查询订单
api.add_resource(getStatus,'/api/get/seller/<seller_id>/order/status/<status>/')


#获取商家信息
api.add_resource(Seller_,'/api/get/seller/msg/<seller_id>/')
#手机端获取所有商家信息,管理端获取商家信息
api.add_resource(getSellers,'/api/get/all/sellers/')
#编辑商家信息
api.add_resource(putSeller,'/api/put/seller/<seller_id>/')
#添加商家信息
api.add_resource(addSeller,'/api/add/seller/')
#前端搜索商家位置
api.add_resource(searchSellers,'/api/search/sellers/')


#获取轮播图
api.add_resource(getCarousels,'/api/get/carousels/')


#获取七牛云token
api.add_resource(Token,'/api/get/qiniu/token/')

#获取用户信息
api.add_resource(getUser,'/api/get/user/info/<user_id>/')

#小程序微信支付
api.add_resource(WXPay,'/api/wxpay/')
#异步回调
api.add_resource(Notify,'/api/notify/')


