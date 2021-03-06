# -*- coding: utf-8 -*-
import pdfplumber
from flask import request, jsonify, send_from_directory
from flask_migrate import MigrateCommand
# from flask_restful import reqparse
from flask_script import Manager
from pptx import Presentation
from App import create_app
# from utrils.aliyunsms.sms_send import send_sms
import os
import shutil
from xlrd import open_workbook
from pydocx import PyDocX
import pdfkit

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
        #.docx文件转成html文件
        html = PyDocX.to_html('./file/{}'.format(file_name))
        f = open('./file/test.html', 'w', encoding="utf-8")
        f.write(html)
        f.close()
        #把html文件转成pdf文件
        pdfkit.from_file('./file/test.html', './file/test.pdf')
        f = pdfplumber.open('./file/test.pdf')
        page = len(f.pages)
        print('pdf页数：', page)

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


# @app.route("/sendsms", methods=["POST"])
# def sms_captcha():
#     parser = reqparse.RequestParser()
#     parser.add_argument(name='phone', type=str)
#     parse = parser.parse_args()
#     phone = parse.get('phone')
#     str = ""
#     for i in range(6):
#         ch = chr(random.randrange(ord('0'), ord('9') + 1))
#         str += ch
#     print(str)
#     params = {'code':str} #abcd就是发发送的验证码，code就是模板中定义的变量
#     result = send_sms(phone, json.dumps(params))
#     print(result)
#     if result:
#         return jsonify(params)
#     else:
#         return '发送失败'


if __name__ == '__main__':

    # manager.run()
    app.run(host='0.0.0.0',port='5000')