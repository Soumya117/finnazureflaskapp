from json2html import *

def html(data, html):
    f_table = json2html.convert(json = data)
    path = "templates/" + html + ".html"
    finn_html= open(path,"w")
    finn_html.write(f_table)
    finn_html.close()
