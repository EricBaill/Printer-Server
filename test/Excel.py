from xlrd import open_workbook

# 读取Excel文件名
file_name = '2.xlsx'
file_d = open_workbook(file_name)
# 获得每个页签对象
list_ = []
for i in range(len(file_d.sheets())):
    # 计算sheet数量
    for sheet in file_d.sheets():
        select_sheet = file_d.sheets()[i]
        rows_num = select_sheet.nrows
    # 得到行数 ,sheet名称
    print(sheet.name,rows_num)
    if sheet.name and rows_num != 0:
        print(i+1)
        list_.append(i)
        print(len(list_))
    else:
        pass
page = len(list_)
print('页数',page)

