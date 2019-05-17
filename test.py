# -*- coding: utf-8 -*-
import os
import shutil

import pdfkit
import pdfplumber
from pydocx import PyDocX

html = PyDocX.to_html('./file/test.docx')
f = open('./file/test.html', 'w', encoding="utf-8")
f.write(html)
f.close()

pdfkit.from_file('./file/test.html', './file/test.pdf')

f = pdfplumber.open('./file/test.pdf')
page = len(f.pages)
print('pdf页数：', page)

# #删除本地存储文件
# delDir = "./file"
# delList = list(os.listdir(delDir))
# for f in delList:
#     filePath = os.path.join(delDir, f)
#     if os.path.isfile(filePath):
#         os.remove(filePath)
#         # print(filePath + " was removed!")
#     elif os.path.isdir(filePath):
#         shutil.rmtree(filePath, True)
#     # print("Directory: " + filePath + " was removed!")
