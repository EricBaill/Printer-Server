# import subprocess
# import pdfkit
#
#
# word_file = "11.doc"
# content = subprocess.check_output(["/usr/local/bin/antiword", word_file],encoding='utf-8')
# print(content)
# print(len(content))
# print(type(content))


# pdfkit.from_url('http://google.com', 'out.pdf')
# pdfkit.from_file('test.html', 'out.pdf')
# pdfkit.from_string('hello', 'str-pdf.pdf')


import chardet

f = open('11.doc','r+')

data = f.read()

print(chardet.detect(data))