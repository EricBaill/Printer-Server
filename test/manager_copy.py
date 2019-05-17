# -*- coding: utf-8 -*-
import json
import random
import time
import pdfplumber
from flask import request, jsonify, send_from_directory
from flask_migrate import MigrateCommand
from flask_restful import reqparse
from flask_script import Manager
from pptx import Presentation
from qiniu import Auth, put_data
from App import create_app
from utrils.aliyunsms.sms_send import send_sms
import os
import shutil
from xlrd import open_workbook

app = create_app('develop')
manager = Manager(app=app)
manager.add_command('db',MigrateCommand)


# 用户上传到服务器，服务器再上传到七牛云
@app.route("/api/file/page/", methods=["GET", "POST"])
def upload_qiniu():
    fp = request.files.get("file")
    file_name = fp.filename
    print(fp)

    #指定存储地点
    UPLOAD_FOLDER = './file'
    fp.save(os.path.join(UPLOAD_FOLDER, file_name))

    f_name = file_name.split('.')[-1]
    if f_name == 'PDF' or f_name == 'pdf':
        f = pdfplumber.open('./file/{}'.format(file_name))
        page = len(f.pages)
        print('pdf页数：',page)

    elif f_name == 'ppt' or f_name == 'pptx' or f_name == 'PPT' or f_name == 'PPTX':
        p = Presentation('./file/{}'.format(file_name))
        page = len(p.slides)
        print('ppt页数',page)

    elif f_name == 'doc' or f_name == 'docx' or f_name == 'DOC' or f_name == 'DOCX':
        # Word转pdf
        # path = './file/{}'.format(file_name)
        # pdf_path = path.replace('doc', 'pdf')
        # w = client.CreateObject("Word.Application")
        # doc = w.Documents.Open(path)
        # doc.ExportAsFixedFormat(pdf_path, 17)
        # doc.Close()
        # w.Quit()
        # print(doc)

        # def excel_pdf(self, path):
        #     # Excel转pdf
        #     pdf_path = path.replace('xls', 'pdf')
        #     xlApp = client.CreateObject("Excel.Application")
        #     books = xlApp.Workbooks.Open(path)
        #     books.ExportAsFixedFormat(0, pdf_path)
        #     xlApp.Quit()

        page = 0

    elif f_name == 'xlsx' or f_name == 'xls' or f_name == 'XLSX' or f_name == 'XLS' or f_name == 'csv' or f_name == 'CSV':
        # 读取Excel文件名
        fileName = './file/{}'.format(file_name)
        file_d = open_workbook(fileName)
        # 获得每个页签对象
        list_ = []
        for i in range(len(file_d.sheets())):
            # 计算sheet数量
            for sheet in file_d.sheets():
                select_sheet = file_d.sheets()[i]
                rows_num = select_sheet.nrows
                # 得到行数 ,sheet名称
                print(sheet.name, rows_num)
                if sheet.name and rows_num != 0:
                    print(i + 1)
                    list_.append(i)
                    page = len(list_)
                    print(page)
                else:
                    pass

        page = page
    else:
        page = 1
        print('图片页数',page)

    #删除本地存储文件
    delDir = "./file"
    delList = list(os.listdir(delDir))
    for f in delList:
        filePath = os.path.join(delDir, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
            print(filePath + " was removed!")
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)
        print("Directory: " + filePath + " was removed!")
    return jsonify(page)

    # 需要填写你的 Access Key 和 Secret Key
    # ak = "x8Wiq7iIUk3mZnuKDG2A5y14HLIHieMYZK3UsJJT"
    # sk = "sYQit3y31B9VIL-vQkUho9toQn0noLcf-UFihcQZ"
    # 构建鉴权对象
    # q = Auth(ak, sk)
    # 要上传的空间
    # bucket_name = 'cloudprint'
    # 上传到七牛后保存的文件名
    # key = 'printer' + '/' + 'files' + '/' + fileName

    # 生成上传 Token，可以指定过期时间等
    # token = q.upload_token(bucket_name, key, 3600)
    # ret, info = put_data(token, key, data=fp.read())

    # policy = {}

    # 3600为token过期时间，秒为单位。3600等于一小时
    # token = q.upload_token(bucket_name, key, 3600, policy)

    # print(token)

    # 如果上传成功
    # if info.status_code == 200:
    #     数据库保存该地址
        # img_url = "http://pqcxj2nyo.bkt.clouddn.com/" + ret.get("key") #七牛云域名（注意：CNAME一定要配置）
        # print(img_url)
    # return jsonify(token)


@app.route("/sendsms", methods=["POST"])
def sms_captcha():
    parser = reqparse.RequestParser()
    parser.add_argument(name='phone', type=str)
    parse = parser.parse_args()
    phone = parse.get('phone')
    str = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    print(str)
    params = {'code':str} #abcd就是发发送的验证码，code就是模板中定义的变量
    result = send_sms(phone, json.dumps(params))
    print(result)
    if result:
        return jsonify(params)
    else:
        return '发送失败'


if __name__ == '__main__':

    # manager.run()
    app.run(host='0.0.0.0',port='5000')