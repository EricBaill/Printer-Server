from zipfile import ZipFile
from bs4 import BeautifulSoup

document=ZipFile('5s.docx')
xml=document.read("word/document.xml")
wordObj=BeautifulSoup(xml.decode("utf-8"))
texts=wordObj.findAll("w:t")
for text in texts:
  print(text.text)
print(len(texts))
