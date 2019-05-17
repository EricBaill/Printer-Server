import os
# from zipfile import ZipFile
# from bs4 import BeautifulSoup
#
# document = ZipFile(new_file)
# xml = document.read("word/document.xml")
# wordObj = BeautifulSoup(xml.decode("utf-8"))
# texts = wordObj.findAll("w:t")
# for text in texts:
#     print(text.text)
# print(len(texts))

def re_name(dir_path, old_file, new_file):
    os.renames(dir_path + "/" + old_file, dir_path + "/" + new_file)


if __name__ == '__main__':
    path = os.getcwd()
    print(path)
    re_name(path, "5.doc", "5s.docx")