from pydocx import PyDocX
html = PyDocX.to_html("docx.docx")
f = open("docx.html", 'w', encoding="utf-8")
f.write(html)
f.close()

